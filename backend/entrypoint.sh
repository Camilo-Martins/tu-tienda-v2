#!/bin/sh
set -e

echo "Waiting for MySQL TCP at $STORE_DB_HOST:$STORE_DB_PORT..."

until nc -z "$STORE_DB_HOST" "$STORE_DB_PORT"; do
  echo "MySQL not ready yet..."
  sleep 2
done

echo "MySQL TCP is available!"

exec "$@"
