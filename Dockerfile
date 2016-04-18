FROM python:2.7

MAINTAINER bhearsum@mozilla.com

WORKDIR /app

# install the requirements into the container first
# these rarely change and is more cache friendly
# ... really speeds up building new containers
COPY requirements.txt /app/
RUN pip install -r requirements.txt

# copy in sources after
# Copying Balrog to /app instead of installing it means that production can run
# it, and we can bind mount to override it for local development.
COPY auslib/ /app/auslib/
COPY ui/ /app/ui/
COPY uwsgi/ /app/uwsgi/
COPY scripts/ /app/scripts/
COPY setup.py version.json /app/
# This script is technically only needed for CI, but it's tiny, and not
# worth forking the Dockerfile over.
COPY run-tests.sh /app/

ENTRYPOINT ["/app/uwsgi/run.sh"]
CMD ["public"]
