VIRTUALENV ?= /usr/bin/virtualenv
PYTHON ?= python
NOSE ?= nosetests
VIRTUALENV_DIR ?= $(error VIRTUALENV_DIR must be set when running virtualenv or ci-tests targets)
TEST_PYTHON ?= $(PYTHON)
REQUIREMENTS=requirements.txt

test:
ifdef VERBOSE
	@echo Running unit tests
	$(NOSE) -v
	@echo Running rules tests
	$(TEST_PYTHON) test-rules.py -v
else 
	@echo Running unit tests
	$(NOSE)
	@echo Running rules tests
	$(TEST_PYTHON) test-rules.py
endif

virtualenv:
	$(PYTHON) $(VIRTUALENV) --no-site-packages $(VIRTUALENV_DIR)
	$(VIRTUALENV_DIR)/bin/pip -q install -r $(REQUIREMENTS)

ci-tests: NOSE=$(VIRTUALENV_DIR)/bin/nosetests
ci-tests: TEST_PYTHON=$(VIRTUALENV_DIR)/bin/python
ci-tests: virtualenv test
