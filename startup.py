import os
import subprocess
import sys

def main():
    # Adiciona o diretório principal do projeto ao PYTHONPATH
    projeto_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(os.path.dirname(projeto_dir))

    # Caminho para o script de ativação da virtualenv
    activate_script = os.path.join(projeto_dir, "venv", "bin", "activate") if sys.platform != "win32" else os.path.join(projeto_dir, "venv", "Scripts", "activate")
    activate_comando = f"activate {os.path.join(projeto_dir, 'venv')} &&" if sys.platform == "win32" else f"source {activate_script}"

    # Configuração do ambiente
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "youtube_downloader.settings")

    # Execute as migrações dentro da virtualenv
    comandos_migracao = [
        f"{activate_comando} python manage.py makemigrations",
        f"{activate_comando} python manage.py migrate"
    ]

    for comando in comandos_migracao:
        command_name = comando.split()[-1]
        try:
            result = subprocess.run(comando, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
            # Exiba a saída do comando
            print(f"Saída do comando {command_name}:\n")
            print(result.stdout)
        except subprocess.CalledProcessError as e:
            # Trate exceções de subprocesso aqui
            print(f"\nErro do comando {command_name}:\n")
            print(e.stderr)

        print("\n" + "=" * 40 + "\n")

    comando_start = f"{activate_comando} python manage.py runserver"

    # Redireciona a saída padrão e a saída de erro para um arquivo
    subprocess.run(comando_start, shell=True, stderr=subprocess.STDOUT)

if __name__ == "__main__":
    main()
