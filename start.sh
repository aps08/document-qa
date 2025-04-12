#! /usr/bin/env bash
set -e

echo "alembic migration start"

~/.local/bin/alembic upgrade head

echo "alembic migration completed"

python app/main.py