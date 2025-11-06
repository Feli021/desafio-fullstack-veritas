from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

# Create your models here.
class Livro(models.Model):
    codigo_livro = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=100, help_text="Título do livro")
    autor = models.CharField(max_length=100, help_text="Autor do livro")
    preco = models.DecimalField(max_digits=10, decimal_places=2, help_text="Preço do livro")

    def __str__(self):
        return f"{self.codigo_livro} - {self.titulo} ({self.autor}) - R$ {self.preco:.2f}"


