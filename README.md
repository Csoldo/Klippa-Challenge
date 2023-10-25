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
* The CLI is able to process a folder, so if the `--file-path` parameter is a folder then the API endpoint is called for every image or pdf file inside that folder
* Project can run in docker
* Configfile options for CLI parameters
* Monitor a folder

## Prerequisites
In order to run this application, you need to have python and pip installed.

## Project setup

### Docker
Assuming you have docker installed, you can run the application in a docker container with the following commands:

```sh
docker build -t klippa --rm . 
docker run -it --name klippa --rm klippa
```

### Local environment

```sh
pip install -r requirements.txt
```

## Execute the CLI command
If you give a folder to the parameter `--file-path`, the application won't stop, but it will constantly monitor that folder and run the scan if a new file is added. If the parameter is a single file, the application scans it and exits.

Either locally, or in the docker container, to see all the information about the scan cli command and its parameters run
```sh
python klippa/cli.py scan --help
```
The `api-key`, `template` and `file-path` flags are mandatory, if you do not provide it as flags, a prompt will ask for them.

To run the script with every flag use the following command
```sh
python klippa/cli.py scan --api-key=your_api_key --template=financial_full --file-path=documents --fast --save-json=output 
```

Here is how you can provide the config parameters in a file (config.json):
```json
{
    "api_key": "api_key",
    "template": "financial_full",
    "fast": true,
    "file_path": "documents",
    "save_json": "output"
}
```