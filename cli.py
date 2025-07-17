import os
import subprocess
import typer
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine.url import make_url
import glob
import re
import shutil

load_dotenv()
app = typer.Typer()

def run_alembic(args, env=None, cwd=None):
    env_vars = os.environ.copy()
    if env:
        env_vars.update(env)
    result = subprocess.run(["alembic"] + args, env=env_vars, cwd=cwd)
    if result.returncode != 0:
        raise typer.Exit(result.returncode)

@app.command()
def create_tenant(schema: str):
    db_url = os.getenv("DATABASE_URL")
    engine = create_engine(db_url)
    with engine.connect() as conn:
        conn.execute(text(f'CREATE SCHEMA IF NOT EXISTS "{schema}"'))
        conn.commit()
    typer.echo(f"✅ Created schema '{schema}'")

@app.command()
def revision_public(message: str = typer.Option(..., "-m", "--message")):
    subprocess.run(["alembic", "revision", "-m", message], check=True, cwd="migrations-org")
    typer.echo("📄 Revision created in migrations-org")

@app.command()
def revision(message: str = typer.Option(..., "-m", "--message")):
    subprocess.run(["alembic", "revision", "-m", message], check=True, cwd="migrations-tenant")
    typer.echo("📄 Revision created in migrations-tenant")

@app.command()
def upgrade_public():
    typer.echo("🚀 Upgrading public schema")
    run_alembic(["upgrade", "head"], cwd="migrations-org")

@app.command()
def upgrade(schema: str):
    typer.echo(f"🚀 Upgrading tenant: {schema}")
    run_alembic(["upgrade", "head"], env={"TENANT_SCHEMA": schema}, cwd="migrations-tenant")

@app.command()
def reset_db():
    db_url = os.getenv("DATABASE_URL")
    url = make_url(db_url)
    admin_url = url.set(database="postgres")
    db_name = url.database
    engine = create_engine(admin_url)
    with engine.connect() as conn:
        conn.execution_options(isolation_level="AUTOCOMMIT")
        conn.execute(text(f"DROP DATABASE IF EXISTS {db_name}"))
        conn.execute(text(f"CREATE DATABASE {db_name}"))
    typer.echo(f"✅ Reset database '{db_name}'")

@app.command()
def reset_migrations():
    for folder in ["migrations-org/versions", "migrations-tenant/versions"]:
        if os.path.exists(folder):
            shutil.rmtree(folder)
        os.makedirs(folder)
    typer.echo("🧹 Cleared migration versions")

if __name__ == "__main__":
    app()