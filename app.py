# -*- coding: utf-8 -*-

import os
from flask import Flask
from flask import request
from flask import abort
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
    if not request.get_json():
        abort(400)

    receive_body = request.get_json(cache=False)
    print(str(receive_body))  # for Debug

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
            print('RECEIVE OPERATION: ' + str(receive))
            continue

        print(receive)
        payload['to'] = receive['content']['from']
        payload['content'] = {
            'contentType': 1,
            'toType': 1,
            'text': 'みゅ？'
        }

        try:
            r = requests.post(endpoint_url,
                              headers=headers,
                              proxies=proxies,
                              json=payload)
            print(str(r))
        except Exception as e:
            print(e)

    return jsonify('OK')


if __name__ == '__main__':
    app.run()
