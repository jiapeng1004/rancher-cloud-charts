#!/bin/sh
# KubePi 套件：登录后自动导入 K3s 集群（幂等）
set -eu

BASE="${KUBEPI_URL:-http://kubepi/kubepi/api/v1}"
USER="${KUBEPI_USER:-admin}"
PASS="${KUBEPI_PASS:-kubepi}"
KC="${KUBECONFIG_FILE:-/output/kubepi-kubeconfig.yaml}"
NAME="${CLUSTER_NAME:-k3s-local}"

apk add --no-cache curl jq >/dev/null

wait_file() {
  i=0
  while [ ! -f "$KC" ]; do
    i=$((i + 1))
    [ "$i" -le 60 ] || { echo "kubeconfig not found: $KC"; exit 1; }
    sleep 2
  done
}

wait_kubepi() {
  i=0
  while ! curl -sf "http://kubepi/" >/dev/null 2>&1; do
    i=$((i + 1))
    [ "$i" -le 60 ] || { echo "KubePi not ready"; exit 1; }
    sleep 2
  done
}

login() {
  curl -sf -X POST "$BASE/sessions" \
    -H 'Content-Type: application/json' \
    -d "{\"username\":\"$USER\",\"password\":\"$PASS\",\"authMethod\":\"jwt\"}"
}

cluster_exists() {
  token=$1
  curl -sf "$BASE/clusters" -H "Authorization: Bearer $token" \
    | jq -e --arg n "$NAME" '.data[]? | select(.name == $n)' >/dev/null 2>&1
}

create_cluster() {
  token=$1
  jq -n --arg name "$NAME" --rawfile config "$KC" \
    '{name:$name, configContentStr:$config, spec:{connect:{direction:"forward"}, authentication:{mode:"configFile"}}}' \
    > /tmp/kubepi-import.json
  http_code=$(curl -s -o /tmp/kubepi-import.resp -w '%{http_code}' -X POST "$BASE/clusters" \
    -H "Authorization: Bearer $token" \
    -H 'Content-Type: application/json' \
    --data @/tmp/kubepi-import.json)
  if [ "$http_code" = "200" ] || [ "$http_code" = "201" ]; then
    echo "cluster '$NAME' imported (HTTP $http_code)"
    return 0
  fi
  echo "import failed (HTTP $http_code): $(cat /tmp/kubepi-import.resp)"
  return 1
}

wait_file
wait_kubepi

token=$(login)
echo "KubePi login ok"

if cluster_exists "$token"; then
  echo "cluster '$NAME' already exists, skip"
  exit 0
fi

create_cluster "$token"
