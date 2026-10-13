import os
from flask import Flask

app = Flask(__name__)


@app.route("/")
def home():
    return "Hello from Naveed's CI/CD Project!"


@app.route("/health")
def health():
    return "Application is healthy"


if __name__ == "__main__":
    host = os.getenv("APP_HOST", "127.0.0.1")
    app.run(host=host, port=5000)
