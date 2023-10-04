import os
from datetime import datetime, timedelta, timezone
from .utils import to_json, load_json

from logging import getLogger, INFO
logger = getLogger(__name__)
logger.setLevel(INFO)

HUB_FUNCTION_NAME = os.environ.get('HUB_FUNCTION_NAME')

def execute(event, mod, result_root_key = None, post_function = None):
    """"""
    try:
        command_id = event.get('request', {}).get('command_id') or 'main'
        with mod(event) as client:
            cmd = getattr(client, command_id)
            result = cmd()

    except Exception as e:
        logger.error(e)
        result = {
            'errors': [
                {
                    'name': e.__class__.__name__,'message': str(e)
                }
            ]
        }

    if result_root_key:
        result = {
            result_root_key: result
        }

    if isinstance(result, dict):
        if not result.get('date_time'):
            dt = datetime.now().astimezone(timezone(timedelta(hours=9)))
            result['date_time'] = dt.replace(microsecond=0).isoformat()

        if not result.get('result_id'):
            result['result_id'] = f'r_{command_id}'

    if post_function:
        post_function(result, event)

    payload = {
        'message_log_id': event.get('message_log_id'),
        'result': result,
        'source': event.get('thing_dest_address'),
        'service_id': event.get('service_id'),
    }
    logger.info(f'payload: {payload}')

    if not event.get('standalone_invoke') and HUB_FUNCTION_NAME:
        invoke = True
        if not payload['message_log_id']:
            logger.error('\'message_log_id\' is not available.')
            invoke = False

        if not payload['thing_dest_address']:
            logger.error('\'thing_dest_address\' is not available.')
            invoke = False

        if not payload['service_id']:
            logger.error('\'service_id\' is not available.')
            invoke = False

        if invoke:
            try:
                import boto3
                client = boto3.client('lambda')
                sts = client.invoke(
                    FunctionName=HUB_FUNCTION_NAME,
                    InvocationType='Event',
                    Payload=to_json(payload),
                )
                del sts['Payload']
                logger.info(f'invoke: {sts}')

            except Exception as e:
                logger.error(e)

    return payload


def handler(event, driver_id, result_root_key = None, post_function = None):
    """"""
    logger.info(f'request: {event}')

    if not isinstance(event, dict):
        raise Exception(f'invalid payload: {event}')

    components = f'drivers.{driver_id}.command.handler'.split('.')
    logger.debug(components)

    mod = __import__(components[0])
    for comp in components[1:]:
        mod = getattr(mod, comp)

    if records := event.get('Records'):
        payload = []
        for record in records:
            body = load_json(record['body'])
            payload.append(execute(body, mod, result_root_key, post_function))
        if len(payload) == 1:
            payload = payload[0]

    else:
        payload = execute(event, mod, result_root_key, post_function)

    return payload
