#!/bin/bash

backend_rc=0
frontend_rc=0
test_suite=$1
shift
# TODO: When we can run docker-compose in Taskcluster, we should use
# docker-compose-test.yml instead of running docker directly.
if [[ "${test_suite}" == "backend" || "${test_suite}" == "" ]]; then
  docker build -t balrogtest -f Dockerfile.dev .
fi
if [[ "${test_suite}" == "frontend" || "${test_suite}" == "" ]]; then
  docker build -t balroguitest -f ui/Dockerfile.dev ui
fi
# We can't use a volume mount in Taskcluster, but we do want to use it
# by default for local development, because it greatly speeds up repeated
# test runs.
if [ -n "${NO_VOLUME_MOUNT}" ]; then
    echo "Running tests without volume mount"
    if [[ "${test_suite}" == "backend" || "${test_suite}" == "" ]]; then
      docker run --rm balrogtest test $@
      backend_rc=$?
    fi
    if [[ "${test_suite}" == "frontend" || "${test_suite}" == "" ]]; then
      docker run --rm balroguitest test $@
      frontend_rc=$?
    fi
else
    echo "Running tests with volume mount"
    if [[ "${test_suite}" == "backend" || "${test_suite}" == "" ]]; then
      docker run --rm -v `pwd`:/app balrogtest test $@
      backend_rc=$?
    fi
    if [[ "${test_suite}" == "frontend" || "${test_suite}" == "" ]]; then
      docker run --rm -v `pwd`/ui:/app balroguitest test $@
      frontend_rc=$?
    fi
fi

if [[ ${backend_rc} == 0 && ${frontend_rc} == 0 ]]; then
  echo "All tests pass!!!"
  exit 0
else
  echo "FAIL FAIL FAIL FAIL FAIL. Some tests failed, see above for details."
  exit 1
fi
