VIRTUALENV=virtualenv
PYTHON=python
NOSE=nosetests
REQUIREMENTS=requirements.txt

test:
	@ifdef VERBOSE
		@echo Running unit tests
		$(NOSE) -v
		@echo Running rules tests
		$(PYTHON) test-rules.py -v
	@else 
		@echo Running unit tests
		$(NOSE)
		@echo Running rules tests
		$(PYTHON) test-rules.py
	@endif

virtualenv:
	virtualenv $(VIRTUALENV_DIR)
	$(VIRTUALENV_DIR)/bin/pip install -r $(REQUIREMENTS)

ci-tests:
	make virtualenv VIRTUALENV_DIR=`mktemp -d`
	make test VERBOSE=1 NOSE=$(VIRTUALENV_DIR)/bin/nosetests \
			  PYTHON=$(VIRTUALENV_DIR)/bin/python
