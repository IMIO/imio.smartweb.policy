#!/usr/bin/make
VENV_FOLDER=.venv

ifeq (, $(shell which uv ))
  $(error "[ERROR] The 'uv' command is missing from your PATH. Install it from: https://docs.astral.sh/uv/getting-started/installation/")
endif

all: buildout

.PHONY: help
help: ## Display this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: buildout
buildout: bin/instance ## Install development environment

.PHONY: run
run: bin/instance ## Start the instance
	bin/instance fg

.PHONY: test
test: bin/instance ## Run tests
	bin/test

.PHONY: test-coverage
test-coverage: bin/instance ## Run tests with coverage
	bin/test-coverage

.PHONY: cleanall
cleanall: ## Clean development environment
	rm -fr .venv pyvenv.cfg develop-eggs downloads eggs parts .installed.cfg lib lib64 include bin .mr.developer.cfg local/

$(VENV_FOLDER):
	@echo "Creating virtual environment with uv"
	uv venv

$(VENV_FOLDER)/bin/buildout: $(VENV_FOLDER) buildout.cfg
	@echo "Installing requirements with uv pip interface"
	uv pip install --python $(VENV_FOLDER)/bin/python -r requirements.txt

bin/instance: $(VENV_FOLDER)/bin/buildout
	@echo "Bootstrapping environment with buildout"
	$(VENV_FOLDER)/bin/buildout
