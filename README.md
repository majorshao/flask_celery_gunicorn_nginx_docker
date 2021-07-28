# Running the solution

In order to run this solution, you just have to install Docker, Docker compose, then :
```
bash run_docker.sh
```

Docker installations needed:

— [Docker Desktop installation]

— [Docker Compose installation](https://docs.docker.com/compose/install/)

## The solution

— The project is structured as follows: Flask app and WSGI entry point are localed in flask_app directory. Nginx and project configuration files are located in nginx directory. Both directories contain Docker files that are connected using docker_compose.yml file in the main directory. 
  
- The small flask app is only responding to GET for specific requests, and return the result. Celery and redis are used in the app. gunicorn is used for production ready purpose.

## To do

- Deploy the app to cloud infrastructure, for example, k8. Use the production database and / or redis in cloud.
- Assign specific DNS for the app server.
- Increase access security.
- Assign more celery workers and gunicorn workers to improve performance under high frequency requests.
- Add worker monitoring services, and process supervision services. Improve request queuing service, using, for example, RabbitMQ; or https://flower.readthedocs.io/en/latest/ or web UI with https://www.ordinarycoders.com/blog/article/django-celery-flower
- Pylint and pytest are not finished. And we can try Pycco and pdoc.