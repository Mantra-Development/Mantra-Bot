#! /bin/sh

if $INITIALIZE_DB = true; then
    echo "Database is initializing"
    aerich init -t mantra.core.tortoise_config.tortoise_config
    aerich init-db
fi

if $MIGRATE_DB = true; then
    echo "Database is migrating"
    aerich migrate
    aerich upgrade
fi

python -m mantra