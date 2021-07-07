import os
import json
import logging
import azure.functions as func

from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError


def main(request: func.HttpRequest,  outputCommandQueue: func.Out[str]) -> func.HttpResponse:
    logging.info('Discord slash command hub received a request.')

    DISCORD_APPLICATION_PUBLIC_KEY = os.environ['DISCORD_APPLICATION_PUBLIC_KEY']
    verify_key = VerifyKey(bytes.fromhex(DISCORD_APPLICATION_PUBLIC_KEY))

    signature = request.headers.get('X-Signature-Ed25519')
    timestamp = request.headers.get('X-Signature-Timestamp')
    body = request.get_body().decode('utf-8')

    # Verify signature
    try:
        verify_key.verify(f'{timestamp}{body}'.encode(),
                          bytes.fromhex(signature))
    except BadSignatureError:
        logging.error('Invalid request signature')
        return func.HttpResponse(status_code=401)

    logging.info('Signature confirmed')

    # Check ping message
    if json.loads(body)['type'] == 1:
        logging.info('PING received')
        logging.info('Return type:1 to response')
        return func.HttpResponse(
            body='{"type":1}',
            status_code=200,
            headers={'Content-Type': 'application/json'})

    # Send to azure storage queue
    outputCommandQueue.set(body)
    logging.info('Successfully send data to queue')

    # Return pending status
    response_body = {
        "type": 5,
        "data": {
            "flags": 64
        }
    }
    return func.HttpResponse(
        body=json.dumps(response_body),
        status_code=200,
        headers={'Content-Type': 'application/json'})
