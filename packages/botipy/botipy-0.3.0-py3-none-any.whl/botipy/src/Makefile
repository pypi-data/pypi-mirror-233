# Makefile for packaging the project. DO NOT EDIT THIS UNLESS YOU KNOW WHAT YOU ARE DOING
# GNU Make 4.4
# Build for both Windows and Linux
# Copyright (C) 2023 Pang Hua Yen
# License MIT
#===================================================================================

# Allow only one "make -f Makefile2" at a time, but pass parallelism
.NOTPARALLEL:

.SUFFIXES: .hpux_make_needs_suffix_list

# Command-line flag to silence nested $(MAKE)
$(VERBOSE)MAKESILENT = -s

#Suppress display of executed commands
$(VERBOSE).SILENT:

#===================================================================================

.DEFAULT_GOAL := help

UNAME := $(shell uname)

ifeq ($(UNAME), Linux)
    PYTHON := $(shell which python3)
	PIP := $(shell which pip)
	VIRTUALENV_COMMAND := sudo apt install python3.10-venv
else
    PYTHON := $(shell which python)
	PIP := $(shell which pip)
	VIRTUALENV_COMMAND := pip install virtualenv
endif

ROOT_DIR:=$(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))

ifneq ($(wildcard $(ROOT_DIR)/.venv/.),)
	VENV_PYTHON = $(ROOT_DIR)/.venv/Scripts/python
else
	VENV_PYTHON = $(PYTHON)
endif

define HELP_BODY
Usage:
  make <command>

Commands:
  delenv                     Delete the current virtual environment.
  newenv                     Create or replace this project's virtual environment.
  syncenv                    Sync this project's virtual environment to the latest
                             dependencies.
endef
export HELP_BODY

delenv:
	rm -rf .venv/
.PHONY: delenv

newenv:
	$(VIRTUALENV_COMMAND)
ifeq ($(UNAME), Linux)
	rm -rf .venv/
	$(PYTHON) -m venv .venv
	$(PYTHON) -m pip install -v -U pip setuptools wheel
	$(MAKE) syncenv
else
	$(PYTHON) -m venv --clear .venv
	$(PYTHON) -m pip install -U pip setuptools wheel
	$(MAKE) syncenv
endif
.PHONY: newenv

syncenv:
ifeq ($(UNAME), Linux)
	.venv/bin/pip3 install -v -r ./requirements.txt
else
	SETUPTOOLS_USE_DISTUTILS=stdlib .venv/Scripts/pip install -r ./requirements.txt
endif
.PHONY: syncenv

help:
	@echo "$$HELP_BODY"
.PHONY: help