VENV := venv

ifeq ($(OS),Windows_NT)
   BIN=$(VENV)/Scripts
else
   BIN=$(VENV)/bin
endif

export PATH := $(BIN):$(PATH)

PROJECT := service
TESTS := tests

IMAGE_NAME := swap_api
CONTAINER_NAME := SWAP_API


# Clean

clean:
	rm -rf .mypy_cache
	rm -rf .pytest_cache
	rm -rf $(VENV)


# Setup
.venv:
	python3 -m venv $(VENV)
	pip3 install -r requirements.txt

setup: .venv


# Format

isort_fix: .venv
	isort $(PROJECT)

format: isort_fix


# Lint

isort: .venv
	isort --check $(PROJECT)

flake: .venv
	flake8 $(PROJECT)

mypy: .venv
	mypy $(PROJECT)

pylint: .venv
	pylint $(PROJECT) --disable=C0116,C0115,C0114,C0301

lint: isort flake mypy pylint


# Test

.pytest:
	pytest -s -v

test: .venv .pytest


# Docker

build:
	docker-compose build

run: build
	docker-compose up -d

# All
dev: setup format lint test
all: setup format lint test run

.DEFAULT_GOAL = run