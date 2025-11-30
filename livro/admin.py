from django.contrib import admin
from django.contrib import messages
from .models import Livros, Categoria, Emprestimos
from datetime import datetime

# Ação Personalizada para Devolução
@admin.action(description='Confirmar Devolução e Atualizar Estoque')
def confirmar_devolucao(modeladmin, request, queryset):
    for emprestimo in queryset:
        # Só executa se o livro AINDA NÃO foi devolvido (data_devolucao vazia)
        if emprestimo.data_devolucao is None:
            
            # 1. Atualiza o Empréstimo (Define a data de hoje)
            emprestimo.data_devolucao = datetime.now()
            emprestimo.devolucao_planejada = False # Limpa o aviso de solicitação
            emprestimo.save()

            # 2. Atualiza o Estoque do Livro
            livro = emprestimo.livro
            livro.quantidade += 1  # Aumenta +1
            livro.emprestado = False # Garante que fica disponível
            livro.save()
            
            # Mensagem de Sucesso (Verde)
            messages.success(request, f"Sucesso! O livro '{livro.nome}' foi devolvido. Estoque agora: {livro.quantidade}")
            
        else:
            # Mensagem de Erro/Aviso (Amarela) se tentar devolver algo que já foi devolvido
            messages.warning(request, f"O livro '{emprestimo.livro.nome}' JÁ TINHA sido devolvido antes. O estoque não foi alterado.")

class EmprestimosAdmin(admin.ModelAdmin):
    # Mostra colunas úteis na lista
    list_display = ('livro', 'nome_emprestado', 'data_emprestimo', 'data_devolucao', 'devolucao_planejada')
    # Filtros laterais para facilitar a busca
    list_filter = ('devolucao_planejada', 'data_devolucao')
    # Adiciona nossa ação personalizada no menu
    actions = [confirmar_devolucao]

# Registra tudo no painel
admin.site.register(Livros)
admin.site.register(Categoria)
admin.site.register(Emprestimos, EmprestimosAdmin)