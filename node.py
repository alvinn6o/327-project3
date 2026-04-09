'''
Step 1 complete (peer registry)

Step 2 /message endpoint to receive messages


'''
import requests
import threading
import time
from flask import Flask, request, jsonify
import uuid
import os

app = Flask(__name__)
node_id = str(uuid.uuid4())
peers = set()
NODE_PORT = int(os.environ.get('NODE_PORT', 5000))
NODE_URL = os.environ.get('NODE_URL', f'http://localhost:{NODE_PORT}')
bootstrap_url = os.environ.get('BOOTSTRAP_URL', 'http://localhost:5000')

# Register with bootstrap node
# Your code here
# registration where node registers to bootstrap with its id and get peer list
def boostrap_register():
    while True:
        try:
            response = requests.post(f'{bootstrap_url}/connect', json={'node': NODE_URL}, timeout=3)
            peer_list = response.json().get('peers', []) # boostrap register response
            for peer in peer_list:
                # don't add self
                if peer != NODE_URL:
                    peers.add(peer)
            print(f"Registered with bootstrap. Known peers: {list(peers)}")
            break  # success
        except requests.RequestException as e:
            print(f"Bootstrap error ({e})")
            time.sleep(5)  # retry for bootstrap

# Discover peers directly
# Your code here
# peer to peer discovery where node gets peer list from bootstrap and other peers
# runs in a loop every 3 seconds so the node stays up to date
def discover_peers():
    while True:
        time.sleep(3)

        # ask bootstrap for the peer list
        try:
            response = requests.get(f'{bootstrap_url}/peers', timeout=3) # get peer list from boostrap
            peer_list = response.json().get('peers', [])
            for peer in peer_list:
                # don't add self
                if peer != NODE_URL:
                    peers.add(peer)
        except requests.RequestException:
            pass

        # then ask each known peer for THEIR peer list (true P2P discovery)
        for peer in list(peers):
            try:
                response = requests.get(f'{peer}/peers', timeout=3)
                peer_list = response.json().get('peers', [])
                for p in peer_list:
                    if p != NODE_URL:
                        peers.add(p)
            except requests.RequestException:
                pass  # peer may be temporarily unreachable


# Receive and send messages
# Your code here
@app.route('/message', methods=['POST'])
def receive_message():
    data = request.get_json()
    sender = data.get('sender', 'unknown')
    msg = data.get('msg', '')

    print(f'Received message from {sender}: {msg}')
    return jsonify({'node': NODE_URL, 'status': 'received'})

# Provide peer list when requested
# Your code here
@app.route('/peers', methods=['GET'])
def get_peers():
    return jsonify({'peers': list(peers)})

# daemon=True stops when the main process exits
threading.Thread(target=boostrap_register, daemon=True).start()
threading.Thread(target=discover_peers, daemon=True).start()

if __name__ == '__main__':
    print(f"Node {node_id}, port {NODE_PORT}")
    app.run(host='0.0.0.0', port=NODE_PORT)

