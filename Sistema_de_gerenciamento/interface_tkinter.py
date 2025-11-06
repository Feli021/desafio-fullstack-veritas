from decimal import Decimal
import os
import django
from tkinter import *
from tkinter import messagebox
from datetime import datetime

# Configurar o ambiente Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Sistema_de_gerenciamento.settings")
django.setup()

from myapp.models import Livro  # Importar o model do app

# ------------------- Funções CRUD -------------------

def limpar_campos():
    entry_titulo.delete(0, END)
    entry_autor.delete(0, END)
    entry_preco.delete(0, END)

def validar_campos(titulo, autor, preco):
    if len(titulo.strip()) < 3:
        messagebox.showerror("Erro", "O título deve ter pelo menos 3 caracteres.")
        return False
    if len(autor.strip()) < 3:
        messagebox.showerror("Erro", "O autor deve ter pelo menos 3 caracteres.")
        return False
    try:
        preco = float(preco)
        if preco <= 0:
            messagebox.showerror("Erro", "O preço deve ser um número positivo.")
            return False
    except ValueError:
        messagebox.showerror("Erro", "Preço inválido. Digite um número.")
        return False
    return True

def cadastrar():
    titulo = entry_titulo.get().strip()
    autor = entry_autor.get().strip()
    preco = entry_preco.get().strip()

    if not validar_campos(titulo, autor, preco):
        return
    try:
        preco = Decimal(preco)
        if preco <= 0:
            messagebox.showerror("Erro", "O preço deve ser maior que zero.")
            return

        # Evita duplicar livros com o mesmo título
        if Livro.objects.filter(titulo__iexact=titulo).exists():
            messagebox.showwarning("Aviso", "Já existe um livro com esse título.")
            return

        novo_livro = Livro(titulo=titulo, autor=autor, preco=preco)
        novo_livro.save()
        messagebox.showinfo("Sucesso", f"Livro '{titulo}' cadastrado com sucesso!")
        limpar_campos()
        gerar_relatorio()
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao cadastrar: {e}")

def consultar():
    titulo = entry_titulo.get().strip()
    if not titulo:
        messagebox.showwarning("Aviso", "Digite o título para consultar.")
        return

    try:
        livro = Livro.objects.get(titulo__iexact=titulo)
        entry_autor.delete(0, END)
        entry_autor.insert(0, livro.autor)

        entry_preco.delete(0, END)
        entry_preco.insert(0, livro.preco)

        messagebox.showinfo("Consulta", f"Livro '{livro.titulo}' encontrado!")
    except Livro.DoesNotExist:
        messagebox.showinfo("Consulta", "Livro não encontrado.")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao consultar: {e}")

def atualizar():
    titulo = entry_titulo.get().strip()
    autor = entry_autor.get().strip()
    preco = entry_preco.get().strip()

    if not validar_campos(titulo, autor, preco):
        return

    try:
        livro = Livro.objects.get(titulo__iexact=titulo)
        livro.autor = autor
        livro.preco = preco
        livro.save()
        messagebox.showinfo("Sucesso", "Livro atualizado com sucesso!")
        gerar_relatorio()
    except Livro.DoesNotExist:
        messagebox.showerror("Erro", "Livro não encontrado para atualizar.")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao atualizar: {e}")

def excluir():
    titulo = entry_titulo.get().strip()
    if not titulo:
        messagebox.showwarning("Aviso", "Digite o título do livro para excluir.")
        return

    if messagebox.askyesno("Confirmação", f"Deseja realmente excluir '{titulo}'?"):
        try:
            livro = Livro.objects.get(titulo__iexact=titulo)
            livro.delete()
            messagebox.showinfo("Sucesso", "Livro excluído com sucesso!")
            gerar_relatorio()
            limpar_campos()
        except Livro.DoesNotExist:
            messagebox.showerror("Erro", "Livro não encontrado para exclusão.")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao excluir: {e}")


def gerar_relatorio():
    """Gera relatório atualizado de todos os livros."""
    try:
        livros = Livro.objects.all().order_by("codigo_livro")
        caminho = os.path.join(os.getcwd(), "relatorio_livros.txt")

        with open(caminho, "w", encoding="utf-8") as f:
            f.write("=== RELATÓRIO DE LIVROS ===\n\n")
            f.write(f"{'Código':<10} | {'Título':<30} | {'Autor':<25} | {'Preço (R$)':>10}\n")
            f.write("-" * 85 + "\n")
            for livro in livros:
                f.write(f"{livro.codigo_livro:<10} | {livro.titulo:<30} | {livro.autor:<25} | {livro.preco:>10.2f}\n")
            f.write("\nÚltima atualização: " + datetime.now().strftime("%d/%m/%Y %H:%M:%S"))

        messagebox.showinfo("Relatório", f"Relatório gerado com sucesso!\nArquivo salvo em:\n{caminho}")

    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao gerar relatório: {e}")

# ------------------- Interface Tkinter -------------------

root = Tk()
root.title("Sistema de Cadastro de Livros")
root.geometry("400x300")
root.resizable(False, False)

# Labels
Label(root, text="Título:").grid(row=1, column=0, padx=10, pady=5, sticky=W)
Label(root, text="Autor:").grid(row=2, column=0, padx=10, pady=5, sticky=W)
Label(root, text="Preço (R$):").grid(row=3, column=0, padx=10, pady=5, sticky=W)

# Entradas
entry_titulo = Entry(root, width=40)
entry_autor = Entry(root, width=40)
entry_preco = Entry(root)


entry_titulo.grid(row=1, column=1, padx=10, pady=5)
entry_autor.grid(row=2, column=1, padx=10, pady=5)
entry_preco.grid(row=3, column=1, padx=10, pady=5)

# Consulta automática ao sair do campo Código
entry_titulo.bind("<FocusOut>", lambda event: consultar())

# Botões
Button(root, text="Cadastrar", width=12, command=cadastrar).grid(row=4, column=0, padx=10, pady=10)
Button(root, text="Consultar", width=12, command=consultar).grid(row=4, column=1, padx=10, pady=10, sticky=W)
Button(root, text="Atualizar", width=12, command=atualizar).grid(row=5, column=0, padx=10, pady=5)
Button(root, text="Excluir", width=12, command=excluir).grid(row=5, column=1, padx=10, pady=5, sticky=W)
Button(root, text="Relatório", width=12, command=gerar_relatorio).grid(row=6, column=0, padx=10, pady=5)
Button(root, text="Limpar", width=12, command=limpar_campos).grid(row=6, column=1, padx=10, pady=5, sticky=W)
Button(root, text="Sair", width=12, command=root.destroy).grid(row=7, column=0, padx=10, pady=5)

root.mainloop()
