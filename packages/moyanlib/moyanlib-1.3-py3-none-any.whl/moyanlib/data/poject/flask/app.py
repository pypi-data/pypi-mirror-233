from flask import Flask,render_template, request
from env import *

app = Flask(__name__, template_folder="html",static_folder="html/statics")

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port={{port}}, debug=True)