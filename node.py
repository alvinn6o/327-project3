'''
Step 1 complete (peer registry)

Step 2 /message endpoint to receive messages


'''
import requests
import threading
import time
from flask import Flask, request, jsonify
import uuid

app = Flask(__name__)
node_id = str(uuid.uuid4())
peers = set()
bootstrap_url = "http://localhost:5000"

# Register with bootstrap node
# Your code here

# registration where node registers to bootstrap with its id and get peer list
def boostrap_register():
    try:
        response = requests.post(f'{bootstrap_url}/connect', json={'node': node_id}, timeout=3)
        peers = response.json().get('peers', []) # boostrap register response
        for peer in peers:
            # don't add self
            if peer != node_id:
                peers.add(peer)
    except requests.RequestException as e:
        print(f"Error with boostrap register: {e}") 

# Discover peers directly
# Your code here

# peer to peer discovery where node gets peer list from bootstrap
def discover_peers():
    try:
        response = requests.get(f'{bootstrap_url}/peers', timeout=3) # get peer list from boostrap
        peers = response.json().get('peers', [])
        for peer in peers:
            # don't add self
            if peer != node_id:
                peers.add(peer)
    except requests.RequestException as e:
        print(f"Error finding peers: {e}")


# Receive and send messages
# Your code here
@app.route('/message', methods=['POST'])
def receive_message():
    data = request.get_json()
    sender = data.get('sender')
    message = data.get('message')

    print(f'{sender} sent: {message}')
    return jsonify({'node': node_id, 'message': 'received'})

# Provide peer list when requested
# Your code here
@app.route('/peers', methods=['GET'])
def get_peers():
    return jsonify({'peers': list(peers)})

