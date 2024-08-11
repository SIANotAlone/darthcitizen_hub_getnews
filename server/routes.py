from async_get_news import *
import logger

import threading
import asyncio
from flask import Blueprint, make_response, jsonify

l = logger.Logger()
mainBP = Blueprint('mainBP', __name__)

def start_fetch_news():
    asyncio.run(main())


@mainBP.route('/update_news', methods=['POST'])
def UpdateNews():

    l.logInfo('update news handler')
    tr = threading.Thread(target=start_fetch_news)
    tr.start()
    response = {
        'update_status': 'ok',
        'code': 200
    }
    return make_response(jsonify(response))