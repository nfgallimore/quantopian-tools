PIP_INDEX_URL = https://pypi.python.org/simple

project_dir := $(realpath $(dir $(lastword $(MAKEFILE_LIST))))

ifneq ($(TRAVIS_JOB_NUMBER),)
egg_info_tag_build := +build$(TRAVIS_JOB_NUMBER)
else
egg_info_tag_build := +dev
endif

ifeq ($(VIRTUAL_ENV)$(CONDA_ENV_PATH),)
$(error must run in a virtualenv)
else
$(info running in virtualenv $(VIRTUAL_ENV)$(CONDA_ENV_PATH))
endif

# find project python source dirs
initpys := $(foreach dir,$(wildcard $(project_dir)/*),$(wildcard $(dir)/__init__.py))
python_source_dirs := $(foreach initpy,$(initpys),$(realpath $(dir $(initpy))))
$(info found python source in $(python_source_dirs))

python_version_full := $(wordlist 2,4,$(subst ., ,$(shell python --version 2>&1)))
python_version_major := $(word 1,${python_version_full})
python_version_minor := $(word 2,${python_version_full})
$(info using python$(python_version_major))

.PHONY: all init install lint test test-unit test-integration build docs clean

all: init install lint test build docs

init:
	pip install -i $(PIP_INDEX_URL) -U setuptools
	pip install -i $(PIP_INDEX_URL) -U pip
	pip install -i $(PIP_INDEX_URL) -U pip-tools

pip_compile = pip-compile -i $(PIP_INDEX_URL) --upgrade --rebuild --annotate --header --no-index $(pip_compile_flags)

install:
	mkdir -p .cache
	$(pip_compile) requirements/py$(python_version_major).txt -o .cache/requirements-py$(python_version_major).txt > /dev/null
	pip-sync -i $(PIP_INDEX_URL) .cache/requirements-py$(python_version_major).txt

pytest_args := -v -l$(foreach dir,$(python_source_dirs), --ignore="$(dir)/migrations/")
pytest_cov := $(foreach dir,$(python_source_dirs), --cov="$(dir)") --cov-report=term-missing --cov-report=html --cov-report=xml --no-cov-on-fail
pytest := PYTHONPATH="$(project_dir)" py.test $(pytest_args)
pytest_targets := "$(project_dir)/tests/" $(foreach dir,$(python_source_dirs), "$(dir)")

lint:
	PYTHONPATH="$(project_dir)" pylint --rcfile="$(project_dir)/pylintrc" --reports=n $(foreach dir,$(python_source_dirs), "$(dir)")
	pep8 --show-source --format=pylint $(python_source_dirs)

test:
	mkdir -p tests/reports
	$(pytest) $(pytest_cov) $(pytest_targets)

test-unit:
	mkdir -p tests/reports
	$(pytest) -m "not integration" $(pytest_targets)

test-integration:
	mkdir -p tests/reports
	$(pytest) -m integration $(pytest_targets)

build:
	python setup.py egg_info --tag-build=$(egg_info_tag_build) bdist_wheel --python-tag=py$(python_version_major)$(python_version_minor)

docs:
	cd docs && make html

clean:
	find $(project_dir) -name '*.pyc' -print -exec rm -r -- {} +
	find $(project_dir) -name '__pycache__' -print -exec rm -r -- {} +
	find $(project_dir) -name '.cache' -print -exec rm -r -- {} +
	find $(project_dir) -name '*.egg-info' -print -exec rm -r -- {} +
	rm -rfv $(project_dir)/.cache
	rm -rfv $(project_dir)/tests/reports
	rm -rfv $(project_dir)/build
	rm -rfv $(project_dir)/dist
	cd docs && make clean
