dev: uvicorn apps.web:app --reload
web: gunicorn -w 1 -k uvicorn.workers.UvicornWorker apps.web:app
