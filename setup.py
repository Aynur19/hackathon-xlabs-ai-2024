import os
import subprocess
import sys
import platform

# Настройки
CONDA_INSTALLER_URL = "https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh"  # Ссылка для Linux
MFA_INSTALL_COMMAND = "conda install -c conda-forge montreal-forced-aligner"
SCRIPTS_TO_RUN = ["script1.py", "script2.py"]  # Список других скриптов-заглушек

if platform.system() == "Windows":
    CONDA_INSTALLER_URL = "https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe"
elif platform.system() == "Darwin":
    CONDA_INSTALLER_URL = "https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-x86_64.sh"

def run_command(command, cwd=None):
    """Выполнение команды в терминале."""
    try:
        result = subprocess.run(command, shell=True, cwd=cwd, check=True, text=True)
        print(f"Команда '{command}' выполнена успешно.")
        return result
    except subprocess.CalledProcessError as e:
        print(f"Ошибка выполнения команды '{command}': {e}")
        sys.exit(1)

def install_conda():
    """Установка Miniconda, если она не установлена."""
    print("Проверка установки Conda...")
    if not shutil.which("conda"):
        print("Conda не установлена. Загрузка установщика...")
        installer_path = "miniconda_installer.sh" if not platform.system() == "Windows" else "miniconda_installer.exe"
        run_command(f"curl -o {installer_path} {CONDA_INSTALLER_URL}")
        
        if platform.system() == "Windows":
            print("Установка Miniconda на Windows...")
            run_command(installer_path)
        else:
            print("Установка Miniconda...")
            run_command(f"bash {installer_path} -b -p $HOME/miniconda")
            os.environ["PATH"] = f"{os.path.expanduser('~')}/miniconda/bin:" + os.environ["PATH"]
        print("Conda установлена.")
    else:
        print("Conda уже установлена.")

def install_mfa():
    """Установка Montreal Forced Aligner через Conda."""
    print("Проверка установки MFA...")
    try:
        run_command("conda --version")  # Проверка наличия Conda
        run_command(MFA_INSTALL_COMMAND)  # Установка MFA
        print("Montreal Forced Aligner установлен.")
    except Exception as e:
        print(f"Ошибка при установке MFA: {e}")
        sys.exit(1)

def run_placeholder_scripts():
    """Запуск заглушек скриптов."""
    for script in SCRIPTS_TO_RUN:
        if os.path.exists(script):
            print(f"Запуск скрипта {script}...")
            run_command(f"python {script}")
        else:
            print(f"Скрипт {script} не найден. Пропуск.")

if name == "__main__":
    # 1. Установка Conda
    install_conda()
    
    # 2. Установка MFA через Conda
    install_mfa()

    # 3. Выполнение других скриптов
    run_placeholder_scripts()