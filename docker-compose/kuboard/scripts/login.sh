#!/bin/sh
# Kuboard SSO 登录，输出 KuboardToken
set -eu
apk add --no-cache curl jq >/dev/null

HOST="${KUBOARD_HOST:-kuboard}"
PORT="${KUBOARD_PORT:-80}"
USER="${KUBOARD_USER:-admin}"
PASS="${KUBOARD_PASS:-Kuboard123}"
BASE="http://${HOST}:${PORT}"

jar=/tmp/kuboard.cookies
rm -f "$jar"

auth_url="${BASE}/sso/auth?access_type=offline&client_id=kuboard-sso&redirect_uri=%2Fcallback&response_type=code&scope=openid%20profile%20email%20groups&state=%2F&connector_id=default"
loc=$(curl -s -D - -o /dev/null "$auth_url" | tr -d '\r' | awk '/^Location:/ {print $2}')
req=$(echo "$loc" | sed -n 's/.*req=\([^&]*\).*/\1/p')
[ -n "$req" ] || { echo "failed to get req from: $loc"; exit 1; }

pass_json=$(printf '{"password":"%s","passcode":""}' "$PASS")
curl -s -c "$jar" -b "$jar" -X POST "${BASE}/sso/auth/default?req=${req}" \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  --data-urlencode "login=${USER}" \
  --data-urlencode "password=${pass_json}" >/dev/null

loc2=$(curl -s -D - -o /dev/null -b "$jar" -c "$jar" "${BASE}/sso/approval?req=${req}" | tr -d '\r' | awk '/^Location:/ {print $2}')
code=$(echo "$loc2" | sed -n 's/.*code=\([^&]*\).*/\1/p')
[ -n "$code" ] || { echo "failed to get code from: $loc2"; exit 1; }

curl -s -D /tmp/kuboard.headers -o /dev/null -b "$jar" -c "$jar" "${BASE}/callback?code=${code}&state=%2F"
token=$(grep -i 'Set-Cookie:' /tmp/kuboard.headers | tr -d '\r' | grep KuboardToken | head -1 | sed 's/.*KuboardToken=\([^;]*\).*/\1/')
[ -n "$token" ] || { echo "KuboardToken not found"; cat /tmp/kuboard.headers; exit 1; }
printf '%s' "$token"
