# README

## Introduction
This is a Python script that provides a command-line interface (CLI) for scanning PDF or image files using the Klippa API. The Klippa API is used for Optical Character Recognition (OCR) processing and text extraction from documents. This code utilizes the Typer library for building the CLI and the Rich library for formatting and displaying the results in a user-friendly way.

## Prerequisites
In order to run this application, you need to have python installed.

This dependencies of this project are managed by `poetry` so it is needed to be able to successfully run the project. You can find more information about poetry here: https://python-poetry.org/docs/

Install poetry
```sh
curl -sSL https://install.python-poetry.org | python3 -
```

To start a virtual shell and install all the dependencies, run the following scripts in the root of the project.
```sh
poetry shell
poetry install
```

## Executing the scipt
To see all the information about the scan cli command and its parameters run
```sh
python klippa/cli.py scan --help
```
The `api-key`, `template` and `file-path` flags are mandatory, if you do not provide it as flags, a prompt will ask for them.

To run the script with every flag use the following command
```sh
python klippa/cli.py scan --api-key=your_api_key --template=financial_full --file-path=documents --fast --save-json=output 
```