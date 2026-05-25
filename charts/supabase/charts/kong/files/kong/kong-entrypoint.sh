#!/bin/bash
set -e

# Generate kong.yml from template using envsubst
envsubst < /usr/local/kong/template.yml > /usr/local/kong/kong.yml

echo "Generated kong.yml:"
cat /usr/local/kong/kong.yml

# Start Kong in foreground mode for containers
exec kong docker-start
