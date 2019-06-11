# -*- coding:utf-8 -*-
from flask import Flask
from router import api

app = Flask(__name__)

api.init_app(app)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5005)

