# mpip/mpip/cli.py
import click
import requests


VERSION = "0.1"
URL = "http://127.0.0.1:8000/api"



@click.version_option(version='0.1.0')  # Update with your tool's version
@click.group()
def mpip():
    pass

# @mpip.command()
# @click.argument('url')
# def get(url):
#     response = requests.get(url)
#     click.echo(response.text)

@mpip.command()
@click.option('--name','-n',help="Mojo Package name like sample.mojopkg")
def get(name):
    try:
        url = f'{URL}/packages/{name}/download/'
        response = requests.get(url)
        if response.status_code == 200:
            with open(f'{name}.mojopkg', 'wb') as file:
                file.write(response.content)
            click.echo(f"{name} Package Downloaded Successfully !")
        else:
            click.echo(f"Error : {response.status_code} - {response.text}")
    except Exception as exp:
        click.echo(f"Error : {str(exp)}")


@click.command()
@click.option("--file_path", "-f", type=click.Path(exists=True))
@click.option("--name", "-n")
@click.option("--token", "-t")
@click.option("--description", "-d", default=None, help="Package Description")
@click.option("--version", "-v")
def post(file_path, name, description, version, token):
    try:
        data = {
            "name": name,
            "description": description if description is not None else "",
            "version": version if version is not None else "",
            "token": token,
        }

        url = f'{URL}/add-package/'
        files = {'package': open(file_path, 'rb')}
        response = requests.post(url, data=data, files=files)

        if response.status_code == 200:
            click.echo(response.text)
        else:
            click.echo(f"Error : {response.status_code} - {response.text}")

    except Exception as exp:
        click.echo(f"Error : {str(exp)}")



@mpip.command()
@click.argument('url')
def put(url):
    response = requests.put(url)
    click.echo(response.text)


@mpip.command()
@click.argument('url')
def patch(url):
    response = requests.patch(url)
    click.echo(response.text)



@mpip.command()
@click.argument('url')
def delete(url):
    response = requests.delete(url)
    click.echo(response.text)




if __name__ == '__main__':
    mpip()
