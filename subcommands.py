import click
import httpx
import os
import json
from encryption import AESEncryption
from utiles import finder
from api_service import APIService, File

BASE_URL="http://127.0.0.1:8000/api/v1/files/"

@click.command()
@click.argument("file_name")
@click.option("--encrypt", type=bool, default=True)
@click.option("--password", type=str)
@click.pass_context
def upload(file_name: str, encrypt: bool, password: str, ctx: click.Context):
    """Upload a new file"""
    
    # find the file
    if not os.path.exists(file_name):
        raise FileNotFoundError("File does not exists")

    if password is None:
        password = ctx.obj["config"]["Credentials"]["password"] 

    # read the file
    with open(file_name, "br+") as file:
        file = file.read()
            
    # encrypt the file
    aes = AESEncryption(password)
    file = aes.encrypt(file)

    # upload the encrypted file
    file = File(name=file_name, content=file)
    id, _ = APIService().create(file)
    click.echo("ID\t\tNAME")
    click.secho(f"{id}\t\t{file_name}")
    

@click.command()
@click.argument("identifier")
def download(identifier:int):
    try:
        id = finder(identifier).id
        file_data = APIService().retrieve(id)

    # decrypt the file
        key = os.environ("KEY")
        aes = AESEncryption(key)
        file_data.content = aes.decrypt(file_data.content)

    except FileNotFoundError as e:
        click.secho(e, fg="red", err=True)
        exit(1)
    except Exception as e:
        raise Exception("an error") from e

    with open(file_data.name, "bw") as file:
        file.write(file_data.content)
    click.echo("ID\t\tNAME")
    click.echo(f"{file_data.id}\t\t{file_data.name}")
    
    
@click.command()
@click.pass_context
def list(ctx: click.Context):
    api_service: APIService = ctx.obj["api_service"]
    data = api_service.list()
    click.echo("ID\t\tNAME")
    for record in data:
        click.secho(f"{record.id}",nl=False, fg="green")
        click.echo(f"\t\t{record.name}")

@click.command()
@click.argument("identifier")
@click.pass_context
def delete(ctx: click.Context, identifier: int):
    try:
        file = finder(identifier)
    except FileNotFoundError as e:
        click.secho(e, fg="red", err=True)
        exit(1)
    api_service: APIService = ctx.obj["api_service"]
    data = api_service.list()
    
    click.echo("ID\t\tNAME")
    click.echo(f"{file.id}\t\t{file.name}")
    click.secho("Are you sure you want to delete this file??[y/N]", fg="red", bold=True)
    answer = input()
    if not ((answer =="y") or (answer == "yes")):
        exit(0)
    api_service.delete(file.id)

def login():
    raise NotImplementedError("Login is not Implemented yet")