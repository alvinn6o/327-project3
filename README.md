# Project 3 P2P Docker

Authors: Alvin Ngo, Jason Tran

PowerShell, project root. If anything is already using these containers or ports, run first:
```powershell
docker compose down
docker rm -f solo node1 node2
```

## Build

```powershell
docker compose build
```

## Phase 1

```powershell
docker run -d -p 5000:5000 --name solo p2p-node
Start-Sleep -Seconds 3
curl.exe http://localhost:5000/
docker rm -f solo
```

## Phase 2

```powershell
docker run -d --name node1 -p 5001:5000 p2p-node
docker run -d --name node2 -p 5002:5000 p2p-node
Start-Sleep -Seconds 3
python -c "import requests; print(requests.post('http://localhost:5002/message', json={'sender':'Node1','msg':'Hello Node2!'}).json())"
docker logs node2
docker rm -f node1 node2
```

## Phase 3

```powershell
docker compose up -d
Start-Sleep -Seconds 8
curl.exe http://localhost:5000/peers
curl.exe http://localhost:5001/
python -c "import requests; print(requests.post('http://localhost:5002/message', json={'sender':'Node1','msg':'Hello Node2!'}).json())"
docker logs node2
docker compose down
```

## Many nodes (assignment “dozens” of peers)

```powershell
docker compose --profile many up -d --scale extra=40
```
