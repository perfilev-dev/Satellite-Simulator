import os
import sys

sys.path.insert(1, os.path.join(os.path.abspath('.'), 'venv/lib/python2.7/site-packages'))


from flask import Flask
app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello World!"

if __name__ == "__main__":
    app.run()
