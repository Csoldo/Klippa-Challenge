# README

## Introduction
This is a Python script that provides a command-line interface (CLI) for scanning PDF or image files using the Klippa API. The Klippa API is used for Optical Character Recognition (OCR) processing and text extraction from documents. This code utilizes the Typer library for building the CLI and the Rich library for formatting and displaying the results in a user-friendly way.

The CLI tool is able to call the OCR API endpoint with the parameters:
* API key as an option (Required)
* Template as an option (Required)
* Path to a file to be processed (Required)
* PDF fast or full extraction modes
* Name of output file where the JSON output is saved (print to console if not provided)

Bonuses:
* The CLI is able to process a folder, so if the `--file-path` parameter is a folder then the API endpoint is called for every image or pdf file inside that folder or any subfolder. This is handy when e.g. you have a folder 2023 with files organized in subfolders for each month of the year.
* If a folder is provided as the file path, all the subsuqent files will be processed in parallel (concurrently).

## Prerequisites
In order to run this application, you need to have python installed.

This dependencies of this project are managed by `poetry` so you need to install it to successfully run the project. You can find more information about poetry here: https://python-poetry.org/docs/

Install poetry
```sh
curl -sSL https://install.python-poetry.org | python3 -
```


## Project setup
Navigate to the root of the project. To start a virtual shell and install all the dependencies, run the following scripts in the root of the project.
```sh
poetry shell
poetry install
```

## Execute the CLI command
To see all the information about the scan cli command and its parameters run
```sh
python klippa/cli.py scan --help
```
The `api-key`, `template` and `file-path` flags are mandatory, if you do not provide it as flags, a prompt will ask for them.

To run the script with every flag use the following command
```sh
python klippa/cli.py scan --api-key=your_api_key --template=financial_full --file-path=documents --fast --save-json=output 
```