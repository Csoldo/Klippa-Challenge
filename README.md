# README

## Introduction
This is a Python script that provides a command-line interface (CLI) for scanning PDF or image files using the Klippa API. The Klippa API is used for Optical Character Recognition (OCR) processing and text extraction from documents. This code utilizes the Typer library for building the CLI and the Rich library for formatting and displaying the results in a user-friendly way.

## Prerequisites
This dependencies of this project are managed by `poetry` so it is needed to be able to successfully run the project. You can find more information about poetry here: https://python-poetry.org/docs/

Install poetry
```sh
curl -sSL https://install.python-poetry.org | python3 -
```

To start a virtual shell and install all the dependencies, run the following scripts.
```sh
poetry shell
poetry install
```

## Executing the scipt
To see all the information about the scan cli command run
```sh
python klippa/cli.py scan --help
```


To run the script with every flag use the following command
```sh
python klippa/cli.py scan --api-key=your_api_key --template=financial_full --file-path=documents --fast --save-json=output 
```

We can also give the required configuration values as prompts after running the command
```sh
python klippa/cli.py scan
```