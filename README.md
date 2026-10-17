# Playwright Assignment

This project contains a small Playwright + pytest automation suite for the Selenium Playground website.

## Project structure

- `tests/` – test cases
- `pages/` – page object model classes
- `utils/` – helper utilities and LambdaTest capability setup
- `conftest.py` – shared pytest fixtures and browser setup
- `requirements.txt` – Python dependencies

## Prerequisites

- Python 3.10+
- A virtual environment is recommended

## Setup

1. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Install Playwright browsers:

   ```bash
   playwright install
   ```

## Run tests

Run all tests:

```bash
pytest
```

Run a single test:

```bash
pytest tests/test_simple_form_demo.py::test_simple_form_demo_displays_entered_message
```

Run a single test locally instead of LambdaTest:

```bash
pytest --local tests/test_simple_form_demo.py::test_simple_form_demo_displays_entered_message
```

## LambdaTest setup

This project is configured to run tests on LambdaTest by default. Set the following environment variables before running tests:

```bash
export LT_USERNAME="your_lambdatest_username"
export LT_ACCESS_KEY="your_lambdatest_access_key"
```

On Windows PowerShell:

```powershell
$env:LT_USERNAME = "your_lambdatest_username"
$env:LT_ACCESS_KEY = "your_lambdatest_access_key"
```

## Notes

- The tests use Playwright page fixtures and the page object model to improve maintainability.
- The suite is organized by user flow and browser capability matrix.
