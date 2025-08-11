# Mixnet User study webapp

This webapp consists of two main components:

1. Python backend, powered by flask, storing results into sqlite
2. A complex JavaScript frontend made to simulate a user collaborating with a study participant.

## Requirements
* sqlite3
* webpack
* python3

## Automerge

The automerge CRDT library is used for resolving concurrent edits in the study.

## Running

Compile the JavaScript component using webpack

```bash
yarn webpack build
```

Having created a virtualenv, install the python requirements and run

```bash
venv/bin/pip3 install -r requirements.txt
venv/bin/flask run 
```
