# registry for nodes
# accept peer connection with POST
'''
Store a list of known peers.
Send and receive messages between nodes

Step 1: Implement Peer Registration (Modify node.py to allow peers to register using a POST request)
Step 2: Enable Peer-to-Peer Messaging (Use a /message endpoint to send and receive messages)
Step 3: Start Multiple Nodes
Step 4: Send a Message Between Nodes
'''
from flask import Flask, request, jsonify

app = Flask(__name__)
peers = []

# allow for peer connections
@app.route('/connect', methods=['POST'])
def connect():
    data = request.get_json()
    node_id = data.get('node_id')
    if node_id and (node_id not in peers):
        # print the node id of peer shown in demo
        print(f"Connected peer: {node_id}")
        peers.append(node_id)

    return jsonify({'peers': peers})

# allow to get list of peers
@app.route('/peers', methods=['GET'])
def get_peers():
    return jsonify({'peers': peers})

# bootstrap server start

if __name__ == '__main__':
    app.run(port=5000) # run on port 5000