VIRTUALENV=/usr/bin/virtualenv
PYTHON=python
NOSE=nosetests
REQUIREMENTS=requirements.txt
VIRTUALENV_DIR=$(error VIRTUALENV_DIR must be set when running virtualenv or ci-tests targets)

test:
ifdef VERBOSE
	@echo Running unit tests
	$(NOSE) -v
	@echo Running rules tests
	$(PYTHON) test-rules.py -v
else 
	@echo Running unit tests
	$(NOSE)
	@echo Running rules tests
	$(PYTHON) test-rules.py
endif

virtualenv:
	$(PYTHON) $(VIRTUALENV) --no-site-packages $(VIRTUALENV_DIR)
	$(VIRTUALENV_DIR)/bin/pip install -r $(REQUIREMENTS)

ci-tests: NOSE=$(VIRTUALENV_DIR)/bin/nosetests
ci-tests: PYTHON=$(VIRTUALENV_DIR)/bin/python
ci-tests: virtualenv test
