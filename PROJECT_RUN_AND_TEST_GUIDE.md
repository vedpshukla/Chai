# FHIR ingest pipeline: simple run and test guide

## What this project is

This project is a Flask-based FHIR ingestion system. In simple words, it receives patient or diagnostic data, checks that the data is valid, transforms it into a standard FHIR structure, and then saves or routes it through a pipeline.

The project is organized like this:

- app startup and route registration: [src/interop/app.py](../src/interop/app.py)
- FHIR processing logic: [src/interop/fhirpipeline](../src/interop/fhirpipeline)
- HTTP endpoints: [src/interop/routes](../src/interop/routes)
- config and database helpers: [src/interop/utils](../src/interop/utils)
- test scripts: [tests](../tests)

## First important note

This is not a standard one-click Python app. It expects:

- Python installed
- required libraries installed
- config file present
- database and auth settings prepared
- test scripts run in a specific way

So the project is real and structured, but it needs setup.

## Step 1: install Python and project dependencies

Open a terminal in the project folder and run:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

If you are on Linux or Mac:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Step 2: prepare config

This project expects a config file named `interop.config` near the app code. In the current repo, the code references this kind of configuration in [src/interop/utils/confighelper.py](../src/interop/utils/confighelper.py).

Typical sections are:

- `jwtsettings`
- `repodb`
- `configdb`
- `msgqueue`

If those settings are not present, the app will not fully work because the system expects MongoDB, Postgres, and JWT information.

## Step 3: start the app

The app is in [src/interop/app.py](../src/interop/app.py), not at the repository root. So the simplest pattern is:

```bash
cd src\interop
python app.py
```

or:

```bash
set basedir=%CD%\src\interop
python src\interop\app.py
```

The app listens on port 8080 by default.

## Step 4: test the app in a simple way

This project does not use a standard pytest suite. It uses custom Python test scripts in [tests](../tests).

### A) Test the core OperationOutcome system

This checks the basic error-response format used across the system.

```bash
python tests\test_fhirpipeline_step1.py
```

What it checks:

- error issues are shaped correctly
- status codes are correct
- OperationOutcome responses stay consistent

### B) Test the pipeline parsing and validation logic

Run the other step tests one by one:

```bash
python tests\test_fhirpipeline_step3.py
python tests\test_fhirpipeline_step4.py
python tests\test_fhirpipeline_step5_6.py
python tests\test_fhirpipeline_step7.py
python tests\test_fhirpipeline_step8.py
python tests\test_fhirpipeline_step9.py
python tests\test_fhirpipeline_step11.py
```

These scripts are designed to verify the separate stages of the FHIR pipeline:

- parse request
- canonicalize
- validate content
- dispatch work
- persist and prepare responses

### C) Test the no-database Diagnostic flow

This is the most important end-to-end test for the diagnostic paths when the real DB is unavailable.

```bash
python tests\test_diagnostic_no_db.py
```

This test verifies:

- Observation creation
- DiagnosticReport creation
- invalid input handling
- bad content-type handling
- transaction and batch Bundle behavior
- DB-down fallback behavior

### D) Test the Observation API flow directly

This is a focused API test for the Observation resource.

```bash
python tests\test_observation_api.py
```

This checks:

- create
- read
- search
- update
- history and vread
- delete
- validation failures

### E) Run the full collection of step tests together

There is a wrapper file to run many tests in one batch:

```bash
python tests\run_pipeline_tests.py
```

This script runs a list of the specific test files and prints totals at the end.

## How to test each part in plain English

### 1) If you want to test the error format

Run:

```bash
python tests\test_fhirpipeline_step1.py
```

This is for the low-level error object system.

### 2) If you want to test the FHIR processing pipeline

Run the step scripts:

```bash
python tests\test_fhirpipeline_step3.py
python tests\test_fhirpipeline_step4.py
python tests\test_fhirpipeline_step5_6.py
python tests\test_fhirpipeline_step7.py
python tests\test_fhirpipeline_step8.py
python tests\test_fhirpipeline_step9.py
python tests\test_fhirpipeline_step11.py
```

These test the internal logic of the pipeline, not the UI or outside services.

### 3) If you want to test real HTTP calls without a database

Run:

```bash
python tests\test_diagnostic_no_db.py
```

This is the best check for route behavior when the database is not available.

### 4) If you want to test a single resource endpoint

Run:

```bash
python tests\test_observation_api.py
```

This simulates a practical API flow and checks the expected response rules.

## Typical manual use

You normally would not run all of this at once in a normal developer flow. A practical order is:

1. install dependencies
2. create config
3. start the app
4. test the basic pipeline file
5. test the no-database diagnostic flow
6. test the specific resource route you changed

## Important warning

If you are using this repo as a fresh project on a clean machine, do not expect a pure `pytest` run to work without extra setup. The repo is designed to be validated with custom scripts and environment configuration.

## Summary

This is a real FHIR pipeline project, but it requires setup and a careful test flow. The cleanest way to understand it is:

- app startup is in [src/interop/app.py](../src/interop/app.py)
- pipeline logic is in [src/interop/fhirpipeline](../src/interop/fhirpipeline)
- route handling is in [src/interop/routes](../src/interop/routes)
- tests are in [tests](../tests)

Use the test scripts in the folder instead of a general pytest run.

No project files were changed while preparing this guide.
