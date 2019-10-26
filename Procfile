dev: uvicorn apps.index.app:app --reload
web: gunicorn -w 1 -k uvicorn.workers.UvicornWorker apps.index.app:app
