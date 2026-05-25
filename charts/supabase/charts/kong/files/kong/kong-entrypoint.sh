#!/bin/bash
set -e

# Generate kong.yml from template using sed for variable substitution
# Replace ${VAR} patterns with environment variable values
sed -e "s|\${SUPABASE_AUTH_HOST}|${SUPABASE_AUTH_HOST}|g" \
    -e "s|\${SUPABASE_AUTH_PORT}|${SUPABASE_AUTH_PORT}|g" \
    -e "s|\${SUPABASE_REST_HOST}|${SUPABASE_REST_HOST}|g" \
    -e "s|\${SUPABASE_REST_PORT}|${SUPABASE_REST_PORT}|g" \
    -e "s|\${SUPABASE_REALTIME_HOST}|${SUPABASE_REALTIME_HOST}|g" \
    -e "s|\${SUPABASE_REALTIME_PORT}|${SUPABASE_REALTIME_PORT}|g" \
    -e "s|\${SUPABASE_STORAGE_HOST}|${SUPABASE_STORAGE_HOST}|g" \
    -e "s|\${SUPABASE_STORAGE_PORT}|${SUPABASE_STORAGE_PORT}|g" \
    -e "s|\${SUPABASE_FUNCTIONS_HOST}|${SUPABASE_FUNCTIONS_HOST}|g" \
    -e "s|\${SUPABASE_FUNCTIONS_PORT}|${SUPABASE_FUNCTIONS_PORT}|g" \
    -e "s|\${SUPABASE_ANALYTICS_HOST}|${SUPABASE_ANALYTICS_HOST}|g" \
    -e "s|\${SUPABASE_ANALYTICS_PORT}|${SUPABASE_ANALYTICS_PORT}|g" \
    -e "s|\${SUPABASE_META_HOST}|${SUPABASE_META_HOST}|g" \
    -e "s|\${SUPABASE_META_PORT}|${SUPABASE_META_PORT}|g" \
    /usr/local/kong/template.yml > /usr/local/kong/kong.yml

echo "Generated kong.yml:"
cat /usr/local/kong/kong.yml

# Start Kong in foreground mode for containers
exec kong docker-start
