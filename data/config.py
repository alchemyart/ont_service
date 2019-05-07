import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ONT_ID_REGISTERED = True

WALLET_PATH = './data/wallet.json'
WALLET_PASSOWRD = 'password'

ONT_API_URL = 'http://40.73.69.106:7088'

GAS_LIMIT = 20000
GAS_PRICE = 500

IDENTITY_LABEL = 'Label'

MYSQL_CONN_STR = 'mysql://root:password@mysql:3306/ggac?charset=utf8'

TIME_ZONE = 'Asia/Shanghai'

DEFAULT_REDIS_HOST = 'redis'
DEFAULT_REDIS_PASSWORD = 'password'
DEFAULT_REDIS_PORT = 6389
DEFAULT_REDIS_DB = '12'

CELERY_RESULT_BACKEND = 'redis'
CELERY_REDIS_PORT = DEFAULT_REDIS_PORT
CELERY_REDIS_PASSWORD = DEFAULT_REDIS_PASSWORD
CELERY_REDIS_HOST = DEFAULT_REDIS_HOST
CELERY_REDIS_DB = DEFAULT_REDIS_DB

CELERY_BROKER_TRANSPORT = 'redis'
CELERY_BROKER_BACKEND = 'redis'
CELERY_BROKER_PORT = DEFAULT_REDIS_PORT
CELERY_BROKER_HOST = DEFAULT_REDIS_HOST
CELERY_BROKER_VHOST = '/'
CELERY_BROKER_PASSWORD = DEFAULT_REDIS_PASSWORD
CELERY_BROKER_DB = DEFAULT_REDIS_DB

CELERY_STATE_DB = DEFAULT_REDIS_DB

CELERYD_CONCURRENCY = 1
CELERY_RESULT_PORT = DEFAULT_REDIS_PORT
CELERY_IGNORE_RESULT = True
CELERY_TASK_RESULT_EXPIRES = 1
CELERY_MAX_CACHED_RESULTS = 1

CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE
CELERYD_LOG_FILE = os.path.join(os.path.join(os.path.join(BASE_DIR, 'logs'), 'celery'), '%n%i.log')
CELERYBEAT_LOG_FILE = os.path.join(os.path.join(os.path.join(BASE_DIR, 'logs'), 'celery'), '%n%i.log')
