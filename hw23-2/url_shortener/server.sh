pkill gunicorn
gunicorn -k uvicorn.workers.UvicornWorker main:app --reload