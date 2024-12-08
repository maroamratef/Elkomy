
from flask import Flask, render_template, request
import hashlib
from Crypto.Hash import keccak, SHA3_256
from hashlib import sha256, md5, blake2b
import cupy  # For GPU hashing fallback support

app = Flask(__name__)


# Define cryptographic hashing methods
def keccak_hash_cpu(data):
    return keccak.new(data.encode()).digest()


def sha3_256_hash_cpu(data):
    return SHA3_256.new(data.encode()).digest()


def sha256_hash_cpu(data):
    return hashlib.sha256(data.encode()).digest()


def md5_hash_cpu(data):
    return hashlib.md5(data.encode()).digest()


def blake2b_hash_cpu(data):
    return hashlib.blake2b(data.encode()).digest()


def choose_hash_algorithm(algorithm, data):
    if algorithm == "keccak":
        return keccak_hash_cpu(data)
    elif algorithm == "sha3_256":
        return sha3_256_hash_cpu(data)
    elif algorithm == "sha256":
        return sha256_hash_cpu(data)
    elif algorithm == "md5":
        return md5_hash_cpu(data)
    elif algorithm == "blake2b":
        return blake2b_hash_cpu(data)
    else:
        return b"Unknown Algorithm"


# Homepage with the UI
@app.route("/", methods=["GET", "POST"])
def home():
    result = ""
    if request.method == "POST":
        wallet_address = request.form.get("wallet_address")
        algorithm = request.form.get("algorithm")
        mined_data = "example data for mining"
        hashed_result = choose_hash_algorithm(algorithm, mined_data)
        result = hashed_result.hex()
    return render_template(
        "index.html", result=result
    )


if __name__ == "__main__":
    app.run(debug=True)
