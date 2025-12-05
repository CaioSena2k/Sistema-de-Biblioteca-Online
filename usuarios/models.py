from django.db import models

#user: caio12
#email: caio@gmail.com
#senha: teste1234

class Usuario(models.Model):
    nome = models.CharField(max_length=30)
    email = models.EmailField()
    senha = models.CharField(max_length=64)
    ativo = models.BooleanField(default=False)
    telefone = models.CharField(max_length=20, null=True, blank=True)
    cpf = models.CharField(max_length=14, null=True, blank=True)
    rua = models.CharField(max_length=100, null=True, blank=True)
    is_admin = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.nome