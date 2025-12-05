from django.db import models    
from datetime import date
import datetime
from django.db.models.base import Model
from usuarios.models import Usuario
from datetime import timedelta


class Categoria(models.Model):
    nome = models.CharField(max_length=30)
    descricao = models.TextField()
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.nome


class Livros(models.Model):
    capa_livro = models.ImageField(upload_to='capas/', blank=True, null=True)
    nome = models.CharField(max_length = 100)
    autor = models.CharField(max_length = 30)
    co_autor = models.CharField(max_length = 30, blank = True)
    data_cadastro = models.DateField(default=date.today)
    emprestado = models.BooleanField(default = False)
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    descricao = models.TextField(blank=True, null=True, verbose_name="Descrição do Produto")
    sobre_autor = models.TextField(blank=True, null=True, verbose_name="Sobre o Autor")
    editora = models.CharField(max_length=50, blank=True, null=True)
    data_publicacao = models.DateField(blank=True, null=True, verbose_name="Data da Publicação")
    edicao = models.CharField(max_length=20, blank=True, null=True, verbose_name="Edição")
    idioma = models.CharField(max_length=30, blank=True, null=True)
    paginas = models.IntegerField(blank=True, null=True, verbose_name="Número de Páginas")
    isbn10 = models.CharField(max_length=10, blank=True, null=True, verbose_name="ISBN-10")
    isbn13 = models.CharField(max_length=13, blank=True, null=True, verbose_name="ISBN-13")
    arquivo_pdf = models.FileField(upload_to='pdfs/', blank=True, null=True, verbose_name="Arquivo PDF do Livro")
    quantidade = models.IntegerField(default=1, verbose_name="Quantidade em Estoque")
  

    class Meta:
        verbose_name = 'Livro'

    def __str__(self):
        return self.nome

class Emprestimos(models.Model):
    choices = (
        ('P', 'Péssimo'),
        ('R', 'Ruim'),
        ('B', 'Bom'),
        ('O', 'Ótimo')
    )
    nome_emprestado = models.ForeignKey(Usuario, on_delete=models.CASCADE, blank = True, null = True)
    nome_emprestado_anonimo = models.CharField(max_length = 30, blank = True, null = True)
    data_emprestimo = models.DateTimeField(default=datetime.datetime.now())
    data_devolucao = models.DateTimeField(blank = True, null = True)
    livro = models.ForeignKey(Livros, on_delete=models.DO_NOTHING)
    avaliacao = models.CharField(max_length=1, choices=choices, null=True, blank=True)
    data_prazo = models.DateField(default=None, null=True, blank=True)
    devolucao_planejada = models.BooleanField(default=False) # Indica que o usuário "devolveu" no site

    def __str__(self) -> str:
        return f"{self.nome_emprestado} | {self.livro}"



