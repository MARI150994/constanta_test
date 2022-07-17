#!/bin/sh

set -e
echo "Apply migrations"
alembic upgrade head
echo "migrations ok"

exec "$@"