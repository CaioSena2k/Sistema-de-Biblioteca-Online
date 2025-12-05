from datetime import date, datetime, timedelta
from django.shortcuts import redirect, render
from django.http import HttpResponse
from usuarios.models import Usuario
from .models import Emprestimos, Livros, Categoria
from .forms import CadastroLivro, CategoriaLivro
from django import forms
from django.db.models import Q


# --- VIEW PRINCIPAL (HOME) ---
def home(request):
    if request.session.get('usuario'):
        usuario_id = request.session.get('usuario')
        usuario = Usuario.objects.get(id=usuario_id)
        status_categoria = request.GET.get('cadastro_categoria')
        
        # Lógica de Pesquisa
        termo_pesquisa = request.GET.get('q')
        if termo_pesquisa:
            livros = Livros.objects.filter(nome__icontains=termo_pesquisa) | Livros.objects.filter(autor__icontains=termo_pesquisa)
        else:
            livros = Livros.objects.all()
        
        total_livros = livros.count()
        form = CadastroLivro()
        form.fields['usuario'].initial = request.session['usuario']
        form.fields['categoria'].queryset = Categoria.objects.filter(usuario=usuario)
        form_categoria = CategoriaLivro()
        usuarios = Usuario.objects.all()

        livros_emprestar = Livros.objects.filter(usuario=usuario).filter(emprestado=False)
        livros_emprestados = Livros.objects.filter(usuario=usuario).filter(emprestado=True)

        return render(request, 'home.html', {'livros': livros,
                                             'usuario_logado': usuario, 
                                             'form': form,
                                             'status_categoria': status_categoria,
                                             'form_categoria': form_categoria,
                                             'usuarios': usuarios,
                                             'livros_emprestar': livros_emprestar,
                                             'total_livro': total_livros,
                                             'livros_emprestados': livros_emprestados})
    else:
        return redirect('/auth/login/?status=2')

# --- DETALHES DO LIVRO ---
def ver_livros(request, id):
    if request.session.get('usuario'):
        livro = Livros.objects.get(id=id)
        usuario_logado = Usuario.objects.get(id=request.session['usuario'])
        
        # Verifica se usuário já tem o livro
        usuario_tem_o_livro = Emprestimos.objects.filter(
            livro=livro, 
            nome_emprestado=usuario_logado, 
            data_devolucao=None
        ).exists()
        
        # Pega o empréstimo específico (para saber prazos e status)
        emprestimo_usuario = Emprestimos.objects.filter(
            livro=livro, 
            nome_emprestado=usuario_logado, 
            data_devolucao=None
        ).first()
        
        emprestimos = Emprestimos.objects.filter(livro=livro)
        
        form = CadastroLivro()
        form.fields['usuario'].initial = request.session['usuario']
        form.fields['categoria'].queryset = Categoria.objects.filter(usuario=usuario_logado)
        form_categoria = CategoriaLivro()
        usuarios = Usuario.objects.all()
        livros_emprestar = Livros.objects.filter(usuario=usuario_logado).filter(emprestado=False)
        livros_emprestados = Livros.objects.filter(usuario=usuario_logado).filter(emprestado=True)
        categoria_livro = Categoria.objects.filter(usuario=usuario_logado)

        return render(request, 'ver_livro.html', {
            'livro': livro,
            'categoria_livro': categoria_livro,
            'emprestimos': emprestimos,
            'usuario_logado': usuario_logado,
            'form': form,
            'id_livro': id,
            'form_categoria': form_categoria,
            'usuarios': usuarios,
            'livros_emprestar': livros_emprestar,
            'livros_emprestados': livros_emprestados,
            'usuario_tem_o_livro': usuario_tem_o_livro,
            'emprestimo_usuario': emprestimo_usuario
        })
        
    return redirect('/auth/login/?status=2')
    
# --- CADASTROS ---
def cadastrar_livro(request):
    if request.method == 'POST':
        form = CadastroLivro(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home') 
        else:
            print(form.errors)
    else:
        form = CadastroLivro()
    return render(request, 'home.html', {'form': form})

def excluir_livro(request, id):
    livro = Livros.objects.get(id=id).delete()
    return redirect('/livro/home')

def cadastrar_categoria(request):
    form = CategoriaLivro(request.POST)
    nome = form.data['nome']
    descricao = form.data['descricao']
    id_usuario = request.POST.get('usuario')
    if int(id_usuario) == int(request.session.get('usuario')):
        user = Usuario.objects.get(id=id_usuario)
        categoria = Categoria(nome=nome, descricao=descricao, usuario=user)
        categoria.save()
        return redirect('/livro/home?cadastro_categoria=1')
    else:
        return HttpResponse('Pare de ser um usuário malandrinho. Não foi desta vez.')

# --- EMPRÉSTIMOS E DEVOLUÇÕES ---    
def cadastrar_emprestimo(request):
    if request.method == 'POST':
        nome_emprestado = request.POST.get('nome_emprestado')
        nome_emprestado_anonimo = request.POST.get('nome_emprestado_anonimo')
        livro_emprestado_id = request.POST.get('livro_emprestado')
        
        # Bloqueio de Inadimplentes
        usuario = Usuario.objects.get(id=request.session['usuario'])
        livros_atrasados = Emprestimos.objects.filter(
            nome_emprestado=usuario,
            data_devolucao=None,
            data_prazo__lt=date.today()
        ).exists()

        if livros_atrasados:
            return HttpResponse("Você tem livros atrasados! Devolva-os antes de pegar novos.")

        livro = Livros.objects.get(id=livro_emprestado_id)

        if livro.quantidade > 0:
            if nome_emprestado_anonimo:
                emprestimo = Emprestimos(nome_emprestado_anonimo=nome_emprestado_anonimo,
                                       livro_id=livro_emprestado_id)
            else:
                emprestimo = Emprestimos(nome_emprestado_id=nome_emprestado,
                                       livro_id=livro_emprestado_id)
            
            emprestimo.data_prazo = date.today() + timedelta(days=15)
            emprestimo.save()

            livro.quantidade -= 1
            if livro.quantidade == 0:
                livro.emprestado = True
            
            livro.save()
            return redirect(f'/livro/ver_livro/{livro_emprestado_id}')
        else:
            return HttpResponse("Sem estoque.")

    return redirect('/livro/home')

def devolver_livro(request):
    id = request.POST.get('id_livro_devolver')
    livro = Livros.objects.get(id=id)
    usuario_logado = Usuario.objects.get(id=request.session['usuario'])
    
    emprestimo = Emprestimos.objects.filter(
        livro=livro, 
        nome_emprestado=usuario_logado, 
        data_devolucao=None
    ).first()
    
    if emprestimo:
        emprestimo.devolucao_planejada = True 
        emprestimo.save()

    return redirect(f'/livro/ver_livro/{id}')

def alterar_livro(request):
    livro_id = request.POST.get('livro_id')
    nome_livro = request.POST.get('nome_livro')
    autor = request.POST.get('autor')
    co_autor = request.POST.get('co_autor')
    categoria_id = request.POST.get('categoria_id')

    try:
        categoria = Categoria.objects.get(id=categoria_id)
        livro = Livros.objects.get(id=livro_id)
    except:
        return redirect('/livro/home/')

    if livro.usuario.id == request.session['usuario']:
        livro.nome = nome_livro
        livro.autor = autor
        livro.co_autor = co_autor
        livro.categoria = categoria
        livro.save()
        return redirect(f'/livro/ver_livro/{livro_id}')
    else:
        return redirect('/auth/sair')

def seus_emprestimos(request):
    usuario = Usuario.objects.get(id=request.session['usuario'])
    emprestimos = Emprestimos.objects.filter(nome_emprestado=usuario)

    return render(request, 'seus_emprestimos.html', {'usuario_logado': usuario,
                                                    'emprestimos': emprestimos})

def processa_avaliacao(request):
    id_emprestimo = request.POST.get('id_emprestimo')
    opcoes = request.POST.get('opcoes')
    id_livro = request.POST.get('id_livro')
    
    try:
        emprestimo = Emprestimos.objects.get(id=id_emprestimo)
        emprestimo.avaliacao = opcoes
        emprestimo.save()
    except:
        pass 
    return redirect(f'/livro/ver_livro/{id_livro}')

# --- FUNÇÕES ADMINISTRATIVAS (CORRIGIDAS) ---

def painel_admin(request):
    usuario_id = request.session.get('usuario')
    if not usuario_id:
        return redirect('/auth/login/')
    
    usuario = Usuario.objects.get(id=usuario_id)
    if not usuario.is_admin:
        return redirect('/livro/home/')

    # 1. PEGA TODOS OS EMPRÉSTIMOS ATIVOS (PARA A TABELA)
    emprestimos = Emprestimos.objects.filter(data_devolucao=None).order_by('data_prazo')
    
    # 2. LÓGICA DE BUSCA
    termo_pesquisa = request.GET.get('q')
    if termo_pesquisa:
        emprestimos = emprestimos.filter(
            Q(livro__nome__icontains=termo_pesquisa) |
            Q(nome_emprestado__nome__icontains=termo_pesquisa) |
            Q(nome_emprestado_anonimo__icontains=termo_pesquisa)
        )

    # 3. ESTATÍSTICAS
    total_ativos = emprestimos.count()
    pendentes_devolucao = emprestimos.filter(devolucao_planejada=True).count()
    
    # 4. LISTA DE USUÁRIOS (PARA OS CARDS)
    usuarios_lista = Usuario.objects.all()
    
    return render(request, 'painel_admin.html', {
        'emprestimos': emprestimos,
        'usuarios': usuarios_lista,
        'usuario_logado': usuario,
        'total_ativos': total_ativos,
        'pendentes_devolucao': pendentes_devolucao
    })

def confirmar_devolucao_site(request, id_emprestimo):
    usuario_id = request.session.get('usuario')
    if not usuario_id:
        return redirect('/auth/login/')
    
    usuario = Usuario.objects.get(id=usuario_id)
    if not usuario.is_admin:
        return redirect('/livro/home/')
        
    emprestimo = Emprestimos.objects.get(id=id_emprestimo)
    
    if emprestimo.data_devolucao is None:
        emprestimo.data_devolucao = datetime.now()
        emprestimo.devolucao_planejada = False 
        emprestimo.save()
        
        livro = emprestimo.livro
        livro.quantidade += 1
        livro.emprestado = False
        livro.save()
        
    return redirect('painel_admin')

def mudar_status_usuario(request, id_usuario):
    usuario_id = request.session.get('usuario')
    if not usuario_id:
        return redirect('/auth/login/')
    
    admin_logado = Usuario.objects.get(id=usuario_id)
    if not admin_logado.is_admin:
        return redirect('/livro/home/')

    alvo = Usuario.objects.get(id=id_usuario)
    
    if alvo.id == admin_logado.id:
        return redirect('painel_admin')

    alvo.is_admin = not alvo.is_admin
    alvo.save()
    
    return redirect('painel_admin')