from typer import Typer
from src.pipeline import run
import os
from dotenv import load_dotenv
from src.core.database import OncoDatabase
from rich.panel import Panel
from rich.spinner import Spinner
from rich.console import Console
from rich.markdown import Markdown
app = Typer()
console = Console()
load_dotenv()
dna_spinner = Spinner("aesthetic", text="[bold cyan]🧬 Processing DNA...")
@app.command()
def main(mutation: str, cancer_type: str):
    input_data = {
        "mutation": mutation,
        "cancer_type": cancer_type
    }
    OncoDatabase.load_data(os.getenv("DATA_DIR"))
    with console.status(dna_spinner):
        

        # explanation = run(input_data)
        explanation = run(input_data)
        md = Markdown(explanation)
        console.print(
            Panel(
                md,
                title = "[bold cyan]Precision Oncology Report[/]",
                border_style="bright_blue",
                padding=(1, 2)
            )
        )
    # print(explanation)

if __name__ == "__main__":
    app()