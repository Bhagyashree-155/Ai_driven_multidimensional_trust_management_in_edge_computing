from flask import Flask, jsonify
import socket
import time
import random

app = Flask(__name__)

@app.route("/")
def home():

    processing = random.uniform(0.05, 0.30)

    time.sleep(processing)

    return jsonify({
        "node": socket.gethostname(),
        "status": "ok",
        "processing_time": processing
    })


@app.route("/health")
def health():
    return "healthy", 200


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000
    )