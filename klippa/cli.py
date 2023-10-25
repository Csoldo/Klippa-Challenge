import typer
from api import KlippaAPI
import json

app = typer.Typer()

# Load configuration values from config.json
config = {}
try:
    with open("config.json", "r") as config_file:
        config = json.load(config_file)
except FileNotFoundError:
    config = {}

@app.command("hello")
def hello(name: str):
    typer.echo(f"Hello {name}")

@app.command("scan")
def apiCall(
    api_key: str = typer.Option(config.get("api_key"), prompt="API Key", help="(Required) API key for authentication"),
    template: str = typer.Option(config.get("template"), prompt="Template", help="(Required) Template for OCR processing"),
    file_path: str = typer.Option(None, prompt=True, help="(Required) Path to the PDF or image file (or directory of files) to be processed)"),
    fast: bool = typer.Option(config.get("fast"), help="Use fast text extraction"),
    save_json: str = typer.Option(None, help="Save the JSON response to a file. Note: do not provide extension. Ex: output"),
    ):
    """Scan a PDF or image file (or directory of files) using the Klippa API"""

    # Update the config.json file with the provided values
    config["api_key"] = api_key
    config["template"] = template
    config["fast"] = fast

    with open("config.json", "w") as config_file:
        json.dump(config, config_file, indent=4)

    api = KlippaAPI(api_key, template, file_path, fast, save_json)
    api.scan()



if __name__ == "__main__":
    app()