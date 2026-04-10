"""
Bootstrap node: central registry for the P2P network.
Nodes register once with POST /connect; GET /peers returns everyone who registered.
"""

from flask import Flask, jsonify, request

app = Flask(__name__)
# Order is stable for JSON output (sorted on read in get_peers / response from connect).
peers = []


@app.route("/connect", methods=["POST"])
def connect():
    # Body: {"node": "http://hostname:5000"} — the node's public URL for other peers.
    data = request.get_json() or {}
    url = data.get("node")
    if url and url not in peers:
        print(f"Connected peer: {url}", flush=True)
        peers.append(url)
    return jsonify({"peers": sorted(peers)})


@app.route("/peers", methods=["GET"])
def get_peers():
    return jsonify({"peers": sorted(peers)})


if __name__ == "__main__":
    # Listen on all interfaces so Docker can publish the port.
    app.run(port=5000, host="0.0.0.0")
