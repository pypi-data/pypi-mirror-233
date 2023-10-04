import dotenv
import typer
from lorcania_cli import collection

dotenv.load_dotenv()

app = typer.Typer()
app.add_typer(collection.app, name="collection")
