"""
P2P node: HTTP API for health check, peer registration, gossip, and messages.
Set BOOTSTRAP_URL (e.g. http://bootstrap:5000) for Phase 3; omit for Phase 1 only.
NODE_URL should match how other containers reach this node (Compose sets it explicitly).
"""

import os
import threading
import time
import uuid

import requests
from flask import Flask, jsonify, request

app = Flask(__name__)
node_id = str(uuid.uuid4())
# Other peers' base URLs (e.g. http://node2:5000), used for gossip and returned by GET /peers.
peers = set()

PORT = int(os.environ.get("PORT", "5000"))
# How this node identifies itself to the bootstrap and to others; must be reachable on the Docker network.
NODE_URL = os.environ.get("NODE_URL", f"http://localhost:{PORT}")
bootstrap_url = os.environ.get("BOOTSTRAP_URL")


def bootstrap_register():
    # Register this node with the bootstrap; merge returned peer list into our set.
    # Retry until the bootstrap is up (Compose may start nodes before bootstrap is ready).
    while True:
        try:
            r = requests.post(
                f"{bootstrap_url}/connect", json={"node": NODE_URL}, timeout=5
            )
            for p in r.json().get("peers", []):
                if p != NODE_URL:
                    peers.add(p)
            print(f"Registered with bootstrap. Known peers: {sorted(peers)}", flush=True)
            break
        except requests.RequestException as e:
            print(f"Bootstrap error ({e})", flush=True)
            time.sleep(5)


def discover_peers():
    # Periodically: refresh from bootstrap, then gossip — ask each known peer for their peer list.
    while True:
        time.sleep(3)
        try:
            r = requests.get(f"{bootstrap_url}/peers", timeout=5)
            for p in r.json().get("peers", []):
                if p != NODE_URL:
                    peers.add(p)
        except requests.RequestException:
            pass
        # Copy so we don't iterate while peers may grow from other threads.
        for peer in list(peers):
            try:
                r = requests.get(f"{peer}/peers", timeout=5)
                for p in r.json().get("peers", []):
                    if p != NODE_URL:
                        peers.add(p)
            except requests.RequestException:
                pass


@app.route("/")
def home():
    # Phase 1 roves the node process is up.
    return jsonify({"message": f"Node {node_id} is running!"})


@app.route("/register", methods=["POST"])
def register():
    # Optional Phase 2: another node tells us its URL so we add it to peers without bootstrap.
    data = request.get_json() or {}
    p = data.get("peer") or data.get("url")
    if p and p != NODE_URL:
        peers.add(p)
    return jsonify({"status": "ok"})


@app.route("/message", methods=["POST"])
def receive_message():
    # Body: {"sender": "...", "msg": "..."} — handout expects logs + {"status": "received"}
    data = request.get_json() or {}
    sender = data.get("sender", "unknown")
    msg = data.get("msg", "")
    print(f"Received message from {sender}: {msg}", flush=True)
    return jsonify({"status": "received"})


@app.route("/peers", methods=["GET"])
def get_peers():
    # Other nodes call this to merge our view into theirs
    return jsonify({"peers": sorted(peers)})


if bootstrap_url:
    # Daemon threads exit when the main process exits
    threading.Thread(target=bootstrap_register, daemon=True).start()
    threading.Thread(target=discover_peers, daemon=True).start()

if __name__ == "__main__":
    print(f"Node {node_id} at {NODE_URL} (listening :{PORT})", flush=True)
    # 0.0.0.0 so Docker port mapping works.
    app.run(host="0.0.0.0", port=PORT)
