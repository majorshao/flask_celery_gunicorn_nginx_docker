import celery
from flask import Flask, request
import requests
from requests.exceptions import HTTPError
from requests.exceptions import Timeout
from requests.adapters import HTTPAdapter
from requests.exceptions import ConnectionError
from etc import settings
import logging
import json
from json import JSONDecodeError
import re, sys, os
from celery import Celery

from celery import current_app

sys.path.append(os.getcwd())

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

app = Flask(__name__)
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

app.logger.info(app.name)

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

current_app.conf.CELERY_ALWAYS_EAGER = True
current_app.conf.CELERY_EAGER_PROPAGATES_EXCEPTIONS = True


@app.route('/', methods=['POST', 'GET'])
def bot():
    if request.method == "GET":
        name_result = get_data.apply_async(args=["name"])
        name_dict = name_result.get()
        name = name_dict.get("data")
        joke_result = get_data.apply_async(args=["joke"])
        joke_dict = joke_result.get()
        joke = joke_dict.get("data")
        old_name = joke_dict.get("payload").get("firstName") + "." + joke_dict.get("payload").get("lastName")
        old_name_nospace = joke_dict.get("payload").get("firstName") + joke_dict.get("payload").get("lastName")
        res_str = re.sub(re.compile("|".join((old_name, old_name_nospace))), name, joke)

        return res_str

    else:
        app.logger.info('Working on other requests.')
        return 'Working on other requests.'


@celery.task()
def get_data(key):  

    search_items = settings.SEARCH_CONFIG[settings.ENVIRONMENT]['ALLOWED_URLS']
    session = requests.Session()

    session.mount(search_items.get(key).get("url"), HTTPAdapter(max_retries=3))

    response = ""

    if key == "name" or key == "joke":

        try:
            response = session.get(search_items.get(key).get("url"),
                                   params=search_items.get(key).get("payload"))

            response.raise_for_status()
        except ConnectionError as ce:
            app.logger.exception(f'Connection error occurred: {ce}')
        except HTTPError as http_err:
            app.logger.exception(f'HTTP error occurred: {http_err}')
        except Timeout:
            app.logger.exception(f'The request timed out')
        except Exception as err:
            app.logger.exception(f'Other error occurred: {err}')
        else:
            app.logger.info('Success!')
    else:
        app.logger.info('The request is not ready yet.')

    try:
        json_data = json.loads(response.text)
    except JSONDecodeError as err:
        app.logger.exception("Response could not be converted to JSON")

    json_response = response.json()

    app.logger.info(json_response)

    result = ""

    if key == "name":
        result = json_response.get("first_name") + " " + json_response.get("last_name")

    if key == "joke":
        result = json_response.get("value").get("joke")

    if result:
        return {"data": result, "payload": search_items.get(key).get("payload")}
    else:
        return {"data": "Not found or error", "payload": ""}


if __name__ == '__main__':
    app.run()
    # The web service should remain responsive under load
    # and be able to support multiple concurrent requests.
