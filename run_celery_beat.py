# run_celery.py

import os
import subprocess
import sys

def activate_virtualenv():
    """Activate the virtual environment."""
    if os.name == 'nt':  # If running on Windows
        activate_script = r'D:\INFomatics\INFomatics\INFomatics_env\Scripts\activate.bat'
        command = f'cmd.exe /c "call {activate_script} && python run_celery_beat.py"'
    else:
        activate_script = os.path.join('venv', 'bin', 'activate')  # Adjust 'venv' to your virtual environment folder
        command = f'bash -c "source {activate_script} && python run_celery_beat.py"'
    
    subprocess.Popen(command, shell=True)

def run_celery_beat():
    command = ['celery', '-A', 'INFomatics', 'beat', '--loglevel=info']
    subprocess.Popen(command)

if __name__ == '__main__':
    # Check if the script is already running within the virtual environment
    if os.getenv('VIRTUAL_ENV') is None:
        activate_virtualenv()
    else:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'INFomatics.settings')
        run_celery_beat()
