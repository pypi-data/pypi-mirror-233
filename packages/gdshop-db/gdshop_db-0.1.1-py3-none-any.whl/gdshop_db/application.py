import typer

from gdshop_db.crm.cli import app as crm

app = typer.Typer()

app.add_typer(crm, name="crm")


if __name__ == "__main__":
    app()
