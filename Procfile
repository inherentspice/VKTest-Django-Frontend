release: python manage.py migrate
web: gunicorn core.asgi:application
worker: python manage.py runworker channel_layer
