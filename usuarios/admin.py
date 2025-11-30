from django.contrib import admin
from .models import Usuario

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    # 1. Colunas que aparecem na tabela
    list_display = ('nome', 'email', 'telefone', 'cpf', 'rua')
    
    # 2. Barra de pesquisa (agora dá pra buscar por CPF também)
    search_fields = ('nome', 'email', 'cpf')
    
    # 3. Impede que o admin mude a senha hash na mão (segurança)
    readonly_fields = ('senha',)
    
    # 4. Removemos o 'list_filter' por enquanto, pois não temos campos de categoria 
    # (como 'ativo' ou 'status') na sua tabela de usuários personalizada.