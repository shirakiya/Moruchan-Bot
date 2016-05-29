# -*- coding: utf-8 -*-

import os
from flask import Flask
from flask import request
from flask import jsonify
import requests

app = Flask(__name__)

# ENV Value
FIXIE_URL = os.getenv('FIXIE_URL')
bot_configuration = {
    'channel_id'     : os.getenv('CHANNEL_ID'),
    'channel_secret' : os.getenv('CHANNEL_SECRET'),
    'mid'            : os.getenv('MID'),
}

# Fixed Value
TOCHANNEL           = '1383378250'
EVENTTYPE_SENDING   = '138311608800106203'
EVENTTYPE_MESSAGE   = '138311609000106303'
EVENTTYPE_OPERATION = '138311609100106403'


@app.route('/callback', methods=['POST'])
def callback():
    receive_body = request.get_json(cache=False)
    app.logger.info(receive_body)

    endpoint_url = 'https://trialbot-api.line.me/v1/events'
    # Custom Header for LINE Bot API
    headers = {
        'Content-type': 'application/json; charset=UTF-8',
        'X-Line-ChannelID': bot_configuration['channel_id'],
        'X-Line-ChannelSecret': bot_configuration['channel_secret'],
        'X-Line-Trusted-User-With-ACL': bot_configuration['mid'],
    }
    # 固定IPからAPI callする必要があり, Heroku Fixie利用のため
    proxies = {'https': FIXIE_URL}
    payload = {
        'to': None,
        'toChannel': TOCHANNEL,
        'eventType': EVENTTYPE_SENDING,
        'content': None,
    }

    for receive in receive_body['result']:
        # Operationに関する処理は一旦無反応で
        if receive['eventType'] == EVENTTYPE_OPERATION:
            app.logger.info('RECEIVE OPERATION: ' + str(receive))
            continue

        payload['to'] = receive['content']['from']
        payload['content'] = {
            'contentType': 1,
            'toType': 1,
            'text': 'みゅ？'
        }

        r = requests.post(endpoint_url,
                          headers=headers,
                          proxies=proxies,
                          json=payload)
        app.logger.info(r)

    return jsonify('OK')


if __name__ == '__main__':
    app.run()
