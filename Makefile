VIRTUALENV ?= /usr/bin/virtualenv
# The Python binary to use when running the virtualenv script. Also used for
# running the tests when TEST_PYTHON isn't provided.
PYTHON ?= python
NOSE ?= nosetests
VIRTUALENV_DIR ?= $(error VIRTUALENV_DIR must be set when running virtualenv or ci-tests targets)
# The Python binary to use when running tests.
TEST_PYTHON ?= $(PYTHON)
# A pip requirements file describing the dependencies that should be installed
# into the virtualenv.
REQUIREMENTS=requirements.txt

ifdef VERBOSE
NOSE_ARGS=-v
TEST_ARGS=-v
endif

# Used to run the tests. Useful for both CI-driven tests and manual ones.
test:
	@echo Running unit tests
	$(NOSE) $(NOSE_ARGS)
	@echo Running rules tests
	$(TEST_PYTHON) test-rules.py $(TEST_ARGS)

# Creates a virtualenv containing all the requirements needed to run tests.
virtualenv:
	$(PYTHON) $(VIRTUALENV) --no-site-packages $(VIRTUALENV_DIR)
	$(VIRTUALENV_DIR)/bin/pip -q install -r $(REQUIREMENTS)

# Run the tests, installing any necessary libraries into a virtualenv.
ci-tests: NOSE=$(VIRTUALENV_DIR)/bin/nosetests
ci-tests: TEST_PYTHON=$(VIRTUALENV_DIR)/bin/python
ci-tests: virtualenv test
