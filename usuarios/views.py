from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Usuario
from hashlib import sha256

def login(request):
    if request.session.get('usuario'):
        return redirect('/livro/home/')
    status = request.GET.get('status')
    return render(request, 'login.html', {'status': status})

def cadastro(request):
    if request.session.get('usuario'):
        return redirect('/livro/home/')
    status = request.GET.get('status')
    return render(request, 'cadastro.html', {'status': status})

# --- FUNÇÃO ALTERADA ---
def valida_cadastro(request):
    nome = request.POST.get('nome')
    senha = request.POST.get('senha')
    email = request.POST.get('email')
    
    # 1. CAPTURANDO OS NOVOS CAMPOS DO HTML
    telefone = request.POST.get('telefone')
    cpf = request.POST.get('cpf')
    rua = request.POST.get('rua')

    usuario = Usuario.objects.filter(email = email)

    if len(nome.strip()) == 0 or len(email.strip()) == 0:
        return redirect('/auth/cadastro/?status=1')

    if len(senha) < 8:
        return redirect('/auth/cadastro/?status=2')

    if len(usuario) > 0:
        return redirect('/auth/cadastro/?status=3')

    try:
        senha = sha256(senha.encode()).hexdigest()
        
        # 2. CRIANDO O USUÁRIO COM TODOS OS DADOS
        usuario = Usuario(nome = nome,
                          senha = senha,
                          email = email,
                          telefone = telefone, # Novo
                          cpf = cpf,           # Novo
                          rua = rua)           # Novo
        usuario.save()

        return redirect('/auth/cadastro/?status=0')
    except:
        return redirect('/auth/cadastro/?status=4')
# -----------------------

def validar_login(request):
    email = request.POST.get('email')
    senha = request.POST.get('senha')

    senha = sha256(senha.encode()).hexdigest()

    usuario = Usuario.objects.filter(email = email).filter(senha = senha)

    if len(usuario) == 0:
        return redirect('/auth/login/?status=1')
    elif len(usuario) > 0:
        request.session['usuario'] = usuario[0].id
        return redirect(f'/livro/home/')

    return HttpResponse(f"{email} {senha}")


def sair(request):
    request.session.flush()
    return redirect('/auth/login/') 

def editar_perfil(request):
    if request.method == 'POST':
        usuario_id = request.session.get('usuario')
        if not usuario_id:
            return redirect('/auth/login/')

        usuario = Usuario.objects.get(id=usuario_id)
        
        # 1. PEGA TODOS OS DADOS (Antigos e Novos)
        nome_novo = request.POST.get('nome_usuario')
        email_novo = request.POST.get('email_usuario')
        telefone_novo = request.POST.get('telefone_usuario') # Novo
        cpf_novo = request.POST.get('cpf_usuario')           # Novo
        rua_nova = request.POST.get('rua_usuario')           # Novo
        senha_nova = request.POST.get('senha_usuario')
        
        # 2. ATUALIZA O OBJETO
        usuario.nome = nome_novo
        usuario.email = email_novo
        usuario.telefone = telefone_novo
        usuario.cpf = cpf_novo
        usuario.rua = rua_nova
        
        # Só muda a senha se digitar algo
        if senha_nova and senha_nova.strip() != "":
            senha_criptografada = sha256(senha_nova.encode()).hexdigest()
            usuario.senha = senha_criptografada
            
        # 3. SALVA NO BANCO
        usuario.save()
        
        return redirect('/livro/home')
    
    return redirect('/livro/home')