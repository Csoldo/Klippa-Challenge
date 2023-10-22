import typer
from api import scan

app = typer.Typer()

@app.command("hello")
def hello(name: str):
    typer.echo(f"Hello {name}")

@app.command("scan")
def apiCall(
    api_key: str = typer.Option(None, prompt=True, help="(Required) API key for authentication"),
    template: str = typer.Option(None, prompt=True, help="(Required) Template for OCR processing"),
    file_path: str = typer.Option(None, prompt=True, help="(Required) Path to the PDF or image file (or directory of files) to be processed)"),
    fast: bool = typer.Option(True, help="Use fast text extraction"),
    save_json: str = typer.Option(None, help="Save the JSON response to a file"),
    ):
    """Scan a PDF or image file (or directory of files) using the Klippa API"""

    scan(api_key, template, file_path, fast, save_json)


if __name__ == "__main__":
    app()