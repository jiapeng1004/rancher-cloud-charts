#!/bin/sh
# Kuboard 套件：SSO 登录后自动导入 K3s 集群（幂等）
set -eu

HOST="${KUBOARD_HOST:-kuboard}"
PORT="${KUBOARD_PORT:-80}"
USER="${KUBOARD_USER:-admin}"
PASS="${KUBOARD_PASS:-Kuboard123}"
KC="${KUBECONFIG_FILE:-/output/kuboard-kubeconfig.yaml}"
NAME="${CLUSTER_NAME:-k3s-local}"
BASE="http://${HOST}:${PORT}"
SCRIPT_DIR=${SCRIPT_DIR:-/scripts}

apk add --no-cache curl jq >/dev/null

wait_file() {
  i=0
  while [ ! -f "$KC" ]; do
    i=$((i + 1))
    [ "$i" -le 60 ] || { echo "kubeconfig not found: $KC"; exit 1; }
    sleep 2
  done
}

wait_kuboard() {
  i=0
  while ! curl -sf "${BASE}/" >/dev/null 2>&1; do
    i=$((i + 1))
    [ "$i" -le 60 ] || { echo "Kuboard not ready: ${BASE}"; exit 1; }
    sleep 2
  done
}

login() {
  sed 's/\r$//' "$SCRIPT_DIR/login.sh" | sh
}

cluster_exists() {
  token=$1
  curl -sf -b "KuboardToken=$token" "${BASE}/kuboard-api/cluster//kind/KubernetesCluster" \
    | jq -e --arg n "$NAME" '.items[]? | select(.metadata.name == $n)' >/dev/null 2>&1
}

create_cluster() {
  token=$1
  jq -n --arg name "$NAME" --rawfile kc "$KC" \
    '{kind:"KubernetesCluster", metadata:{name:$name}, spec:{importType:"kubeconfig", kubeconfig:$kc, apiServerUrl:"https://k3s-server:6443"}}' \
    > /tmp/kuboard-import.json
  http_code=$(curl -s -o /tmp/kuboard-import.resp -w '%{http_code}' -X POST \
    "${BASE}/kuboard-api/cluster/${NAME}/kind/KubernetesCluster" \
    -H 'Content-Type: application/json' \
    -b "KuboardToken=$token" \
    --data @/tmp/kuboard-import.json)
  if [ "$http_code" = "200" ] || [ "$http_code" = "201" ]; then
    echo "cluster '$NAME' imported (HTTP $http_code)"
    return 0
  fi
  echo "import failed (HTTP $http_code): $(cat /tmp/kuboard-import.resp)"
  return 1
}

wait_file
wait_kuboard

token=$(login)
echo "Kuboard login ok"

if cluster_exists "$token"; then
  echo "cluster '$NAME' already exists, skip"
  exit 0
fi

create_cluster "$token"
