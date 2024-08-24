# run_celery.py

import os
import subprocess
import sys

def activate_virtualenv():
    """Activate the virtual environment."""
    if os.name == 'nt':  # If running on Windows
        activate_script = r'D:\INFomatics\INFomatics\INFomatics_env\Scripts\activate.bat'
        return activate_script
    else:
        activate_script = os.path.join('venv', 'bin', 'activate')  # Adjust 'venv' to your virtual environment folder
        return activate_script

def run_celery_worker():
    """Start Celery worker in a new terminal."""
    if os.name == 'nt':  # If running on Windows
        command = f'start cmd /k call {activate_virtualenv()} && celery -A myproject worker --loglevel=info --pool=solo'
    else:
        command = f'gnome-terminal -- bash -c "source {activate_virtualenv()} && celery -A myproject worker --loglevel=info --pool=solo"'
    subprocess.Popen(command, shell=True)

def run_celery_beat():
    """Start Celery beat in a new terminal."""
    if os.name == 'nt':  # If running on Windows
        command = f'start cmd /k call {activate_virtualenv()} && celery -A myproject beat --loglevel=info --pool=solo'
    else:
        command = f'gnome-terminal -- bash -c "source {activate_virtualenv()} && celery -A myproject beat --loglevel=info --pool=solo"'
    subprocess.Popen(command, shell=True)

if __name__ == '__main__':
    # Run Celery worker and beat in separate terminals
    run_celery_worker()
    run_celery_beat()
