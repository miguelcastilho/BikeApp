from flask import Flask
import os

app = Flask(__name__)

port = int(os.getenv("PORT", 9000))

@app.route('/')
def test():
    return 'Hello World'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)