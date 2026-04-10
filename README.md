# Project 3 P2P Docker

Authors: Alvin Ngo, Jason Tran

If ports or names are busy:

```powershell
docker compose down
docker rm -f solo node1 node2 bootstrap
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

## Phase 3 — Many nodes (PowerShell)

Uses ports **5000** (bootstrap) and **5001–5020**. Free them first (`docker compose down`, remove old `bootstrap` / `node*`).

Network and bootstrap:

```powershell
docker network create p2p-net
docker run -d --name bootstrap --network p2p-net -p 5000:5000 bootstrap-node
```

20 nodes:

```powershell
for ($i = 1; $i -le 20; $i++) {
  $port = 5000 + $i
  docker run -d --name "node$i" --network p2p-net `
    -p "${port}:${port}" `
    -e "PORT=$port" `
    -e "NODE_URL=http://node${i}:$port" `
    -e "BOOTSTRAP_URL=http://bootstrap:5000" `
    p2p-node
}
```

Random messages:

```powershell
for ($k = 1; $k -le 15; $k++) {
  $src = Get-Random -Minimum 1 -Maximum 21
  $dst = Get-Random -Minimum 1 -Maximum 21
  if ($src -eq $dst) { continue }
  $targetPort = 5000 + $dst
  Write-Host "Sending from node$src to node$dst"
  $body = @{ sender = "node$src"; msg = "Hello node$dst" } | ConvertTo-Json
  Invoke-RestMethod -Uri "http://localhost:$targetPort/message" -Method Post -Body $body -ContentType "application/json"
}
```

Cleanup:

```powershell
docker rm -f bootstrap
for ($i = 1; $i -le 20; $i++) { docker rm -f "node$i" }
docker network rm p2p-net
```

If `p2p-net` already exists from a previous run, skip `docker network create` or remove the old network after cleanup.
