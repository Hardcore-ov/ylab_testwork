import os

from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.environ.get('POSTGRES_HOST')
DB_PORT = os.environ.get('POSTGRES_PORT')
DB_NAME = os.environ.get('POSTGRES_DB')
DB_USER = os.environ.get('POSTGRES_USER')
DB_PASS = os.environ.get('POSTGRES_PASSWORD')

DATABASE_URL = f'postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

TEST_DATABASE_URL = os.environ.get('TEST_DATABASE_URL')

TEST_ASYNC_DATABASE_URL = os.environ.get('TEST_ASYNC_DATABASE_URL')

BROKER_USER = os.getenv('RABBITMQ_USER')
BROKER_PASSWORD = os.getenv('RABBITMQ_PASSWORD')
BROKER_HOST = os.getenv('RABBITMQ_HOST')

BROKER_URL = f'amqp://{BROKER_USER}:{BROKER_PASSWORD}@{BROKER_HOST}//'
BROKER_BACKEND = 'rpc://'

# CELERY settings
CELERY_BROKER_URL = BROKER_URL
CELERY_BROKER_TRANSPORT_OPTION = {'visibility_timeout': 3600}
CELERY_RESULT_BACKEND = BROKER_BACKEND
CELERY_ACCEPT_CONTENT = ['application/json', 'application/x-python-serialize']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERYD_MAX_TASKS_PER_CHILD = 4
