from flask import Flask
from flask import jsonify

import blockchain
import wallet

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    # option
    # 実装パターン
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5000,
                        type=int, help='port to liston on')
    args = parser.parse_args()
    port = args.port

    app.run(host='0.0.0.0', port=port, threaded=True, debug=True)