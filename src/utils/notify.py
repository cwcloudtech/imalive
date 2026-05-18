import os
import requests

from utils.common import is_empty, is_empty_key, is_not_empty
from utils.logger import log_msg

_node_name = os.environ['IMALIVE_NODE_NAME']
_webhook_url = os.getenv('WEBHOOK_URL')
_webhook_auth_header_name = os.getenv('WEBHOOK_AUTH_HEADER_NAME')
_webhook_auth_header_value = os.getenv('WEBHOOK_AUTH_HEADER_VALUE')

def notify(level, payload):
    if is_empty(payload):
        payload = {}

    if is_empty_key(payload, 'node'):
        payload['node'] = _node_name 

    log_msg(level, payload)

    headers = {
        'Content-Type': 'application/json'
    }

    if is_not_empty(_webhook_auth_header_name) and is_not_empty(_webhook_auth_header_value):
        headers[_webhook_auth_header_name] = _webhook_auth_header_value

    if is_not_empty(_webhook_url):
        requests.post(_webhook_url, json=payload, headers=headers)
