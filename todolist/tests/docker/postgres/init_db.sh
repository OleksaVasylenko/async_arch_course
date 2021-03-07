#!/usr/bin/env bash

set -ex

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" -f /fixtures/10-users.sql
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" -d "testdb" -f /fixtures/20-tables.sql
