@echo off
set PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python
conda activate flask_api
cd "D:\INFomatics\INFomatics with media"
start cmd /k "celery -A INFomatics worker --pool=solo -l info"
start cmd /k "celery -A INFomatics beat -l info"
pause
