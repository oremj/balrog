#!/bin/bash

if [ $1 == "public" ]; then
   exec uwsgi --ini /app/uwsgi/public.ini --python-autoreload 1
elif [ $1 == "admin" ]; then
   exec uwsgi --ini /app/uwsgi/admin.ini --python-autoreload 1
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
    if [ -z "${OUTPUT_FILE}" ]; then
        echo "\${OUTPUT_FILE} must be set!"
        exit 1
    fi
    python scripts/manage-db.py -d ${DBURI} extract dump.sql
    xz -T0 -zc dump.sql > ${OUTPUT_FILE}
elif [ $1 == "reset-stage-db" ]; then
    if [ -z "${DBURI}" ]; then
        echo "\${DBURI} must be set!"
        exit 1
    fi
    if [ -z "${2}" ]; then
        echo "magic word must be passed as second positional argument"
        exit 1
    fi
    exec scripts/reset-stage-db.sh $DBURI $2
elif [ $1 == "create-local-admin" ]; then
    if [ -z "${LOCAL_ADMIN}" ]; then
        echo "\$LOCAL_ADMIN must be set to whatever account you intend to login with. If you don't know what this is, you should ask."
        exit 1
    fi
    # Protect against this accidentally (or maliciously) being used in prod
    if [ "${DB_HOST}" != "balrogdb" -a "${DB_HOST}" != "balrogdb-py3" ]; then
        echo "create-local-admin cannot be used outside of local development"
        exit 1
    fi
    mysql -h $DB_HOST -u balrogadmin --password=balrogadmin -e "insert into permissions (username, permission, data_version) values (\"${LOCAL_ADMIN}\", \"admin\", 1)" balrog
    mysql -h $DB_HOST -u balrogadmin --password=balrogadmin -e "insert into user_roles (username, role, data_version) values (\"${LOCAL_ADMIN}\", \"releng\", 1)" balrog
    exit $?
elif [ $1 == "sync-to-gcs" ]; then
    if [ -z "${BALROG_API_URL}" ]; then
        echo "\${BALROG_API_URL} must be set!"
        exit 1
    fi
    if [ -z "${RELEASES_HISTORY_BUCKET}" ]; then
        echo "\${RELEASES_HISTORY_BUCKET} must be set!"
        exit 1
    fi
    if [ -z "${GOOGLE_APPLICATION_CREDENTIALS}" ]; then
        echo "\${GOOGLE_APPLICATION_CREDENTIALS} must be set!"
        exit 1
    fi
    python scripts/releases-history-to-gcs.py ${BALROG_API_URL} ${RELEASES_HISTORY_BUCKET}
    exit $?
elif [ $1 == "test" ]; then
    coveralls=1
    cd /app
    tox
    rc=$?
    if [[ $rc == 0 ]]; then
        echo "All tests pass!!!"
    else
        echo "FAIL FAIL FAIL FAIL FAIL FAIL FAIL FAIL. Some tests failed, see above for details."
    fi
    # Only send coverage data for the authoritative Balrog repo.
    if [[ $GITHUB_BASE_REPO_URL == "https://github.com/mozilla/balrog.git" ]];
    then
        # COVERALLS_REPO_TOKEN is already in the environment
        export CIRCLECI=1
        export CI_PULL_REQUEST=$GITHUB_PULL_REQUEST
        cd /app
        coveralls
    fi
    exit $rc
else
   echo "unknown mode: $1"
   exit 1
fi
