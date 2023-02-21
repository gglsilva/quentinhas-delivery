## run rabbitmq with docker

> docker run --rm -it --hostname my-rabbit -p 15672:15672 -p 5672:5672 rabbitmq:3-management

## run celery
celery -A config worker -Q celery

## run flower
celery -A config flower
