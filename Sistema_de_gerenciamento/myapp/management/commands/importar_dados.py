import os
import django
import pandas as pd
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
#Configuração Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Sistema_de_gerenciamento.settings")
django.setup()
from myapp.models import Departamento, Categoria, Patrimonio

# Caminho do arquivo CSV Patrimonios
CSV_PATH = r"C:\Users\HP\Desktop\Algoritmos HackerRank\Projeto Rad\Sistema_de_gerenciamento\myapp\tabela.csv"  

class Command(BaseCommand):
    help = "Importa dados do CSV para o modelo Patrimonio"
    def handle(self, *args, **options):
    #Funções para o arquivo de Patrimonios
        def extract_data():
            self.stdout.write("Extraindo dados do CSV...")
            df = pd.read_csv(CSV_PATH, sep=',', encoding='utf-8')
            self.stdout.write(f"{len(df)} linhas carregadas.")
            return df

        def transform_data(df):
            self.stdout.write("Tratando dados...")
            #  remover linhas nulas
            df = df.dropna(subset=['nome', 'valor'])

            # Converter tipos
            df['valor'] = df['valor'].astype(str).str.replace(',', '.').str.strip()
            df['valor'] = df['valor'].astype(float)

            # Normalizar strings
            df['nome'] = df['nome'].str.strip().str.title()
            df.columns = df.columns.str.strip().str.lower()

               # Ordenar pelo numero_patrimonio
            df = df.sort_values(by='numero_patrimonio')

            self.stdout.write("Tratamento concluído.")
            return df

        def load_data(df):
            self.stdout.write("Carregando dados no banco de dados...")
            for _, row in df.iterrows():
                categoria_obj, _ = Categoria.objects.get_or_create(nome=row['categoria'])
                departamento_obj, _ = Departamento.objects.get_or_create(nome=row['departamento'])
                try:
                    responsavel_obj = User.objects.get(username=row['responsavel'])
                except User.DoesNotExist:
                    responsavel_obj = None  # campo permite null

                Patrimonio.objects.update_or_create(
                    numero_patrimonio=row['numero_patrimonio'],
                    defaults={
                        'nome': row['nome'],
                        'descricao': row['descricao'],
                        'categoria': categoria_obj,
                        'departamento': departamento_obj,
                        'localizacao': row['localizacao'],
                        'responsavel': responsavel_obj,
                        'data_aquisicao': row['data_aquisicao'],
                        'valor': row['valor'],
                        'status': row['status']
                    }
                )

            # Delete após inserir/atualizar
            deletados = Patrimonio.objects.filter(status='BAIXADO').delete()
            self.stdout.write(f" Patrimônios deletados (status BAIXADO): {deletados[0]}")

            self.stdout.write("Dados carregados com sucesso!")
        df = extract_data()
        df = transform_data(df)
        load_data(df)



