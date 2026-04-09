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
# Discover peers directly
# Your code here
# Receive and send messages
# Your code here
# Provide peer list when requested
# Your code here