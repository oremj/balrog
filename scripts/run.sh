#!/bin/bash

run_back_end_tests() {
  cd /app
  tox $@
}

if [ $1 == "public" ]; then
   exec uwsgi --ini /app/uwsgi/public.ini --python-autoreload 1
elif [ $1 == "admin" ]; then
   exec uwsgi --ini /app/uwsgi/admin.ini --python-autoreload 1
elif [ $1 == "admin-dev" ]; then
    exec uwsgi --ini /app/uwsgi/admin.dev.ini --ini /app/uwsgi/admin.ini --python-autoreload 1
elif [ $1 == "create-db" ]; then
    if [ -z "${DBURI}" ]; then
        echo "\${DBURI} must be set!"
        exit 1
    fi
    exec python scripts/manage-db.py -d ${DBURI} create
elif [ $1 == "upgrade-db" ]; then
    if [ -z "${DBURI}" ]; then
        echo "\${DBURI} must be set!"
        exit 1
    fi
    exec python scripts/manage-db.py -d ${DBURI} upgrade
elif [ $1 == "cleanup-db" ]; then
    if [ -z "${DBURI}" ]; then
        echo "\${DBURI} must be set!"
        exit 1
    fi
    if [ -z "${MAX_AGE}" ]; then
        echo "\${MAX_AGE} must be set!"
        exit 1
    fi
    if [ -z "${DELETE_RUN_TIME}" ]; then
        echo "\${DELETE_RUN_TIME} must be set!"
        exit 1
    fi

    exec scripts/run-batch-deletes.sh $DBURI $MAX_AGE $DELETE_RUN_TIME
elif [ $1 == "extract-active-data" ]; then
    if [ -z "${DBURI}" ]; then
        echo "\${DBURI} must be set!"
        exit 1
    fi
    exec python scripts/manage-db.py -d ${DBURI} extract ${OUTPUT_FILE}
elif [ $1 == "test" ]; then
    cd /app
    tox $@
else
   echo "unknown mode: $1"
   exit 1
fi
