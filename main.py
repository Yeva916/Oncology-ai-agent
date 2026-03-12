from typer import Typer
from src.pipeline import run
import os
from dotenv import load_dotenv
from src.core.database import OncoDatabase
from rich.panel import Panel
from rich.spinner import Spinner
from rich.console import Console
from rich.markdown import Markdown
from rich.table import Table
from rich.console import Group

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
        

  
        result = run(input_data) 
    

    table = Table.grid(padding=(0, 2))
    table.add_column(style="bold cyan", justify="right") 
    table.add_column(style="white")                     
    
    table.add_row("Gene:", result.get("gene"))
    table.add_row("Mutation:", result.get("mutation"))
    table.add_row("Cancer Type:", result.get("cancer_type"))
    table.add_row("Recommended Therapy:", f"[bold green]{result.get('recommended_therapy')}[/]")
    table.add_row("Evidence Level:", result.get("evidence_level"))

  
    report_content = Markdown(f"### Explanation\n{result.get('mutation_description')}")
    
    console.print(
        Panel(
            
            Group(table, "\n", report_content),
            title="[bold cyan]Precision Oncology Report[/]",
            border_style="bright_blue",
            padding=(1, 2)
        )
    )
    

if __name__ == "__main__":
    app()