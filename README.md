### Jobify - A scraper for job search

_Jobify is a python3 powered script which scrapes from career site_

Currently supported sites:
1. Spotify

## 1. Create virtual environment
 - Move to folder: `cd jobify`
 - Run the command: `python3 -m venv .venv`
 - Activate venv: `source .venv/bin/activate`

## 2. Running Your Project
Install Poetry (if not already installed):
 - `curl -sSL https://install.python-poetry.org | python3 -`

## 3. Install Dependencies:
Navigate to your project directory and run:
 - `poetry install`

## 4. Run Your Project:
Use the following command to run your job scraper:
 - `poetry run job-scraper`

## 5. Run Tests.
Use the following command for running test cases under `tests/` directory
 - `python -m unittest jobify/tests/test_scraper.py` 

## Contributions
**Scrapers are welcomed!!** 
 - New source contributions are welcomed with either using `selenium` or `bs4` which scrapes job sites. Only limit is it should a job site listed with careers oppurtunities. 
 - New sources should be added under `sources/` directory and update the `config.py` with the url and name
 - Capitalize the first letter of company while naming the files under sources.

## Run format after contribution
Run the following for formatting the code while raising a PR
`poetry run format`