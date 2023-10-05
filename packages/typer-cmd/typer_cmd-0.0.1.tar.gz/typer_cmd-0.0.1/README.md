# typer-shell

typer-shell is an extension to typer that easily turns your typer app into a shell utility. It is built on top of the built in python cmd module, with modifications to make it work with typer.


## Usage

Simply create a Typer instance and add it into the TyperCmd instance:

```python
import typer
from typer_shell.shell import TyperCmd


app = typer.Typer()

job_app = typer.Typer()
app.add_typer(job_app, name="job")


@app.command()
def hello(name: str):
    print("hello", name)


@job_app.command()
def run(name: str):
    print(f'run job {name}')


@job_app.command()
def list():
    print('list jobs')


if __name__ == "__main__":
    cmd = TyperCmd(typer=app)
    cmd.cmdloop()

```

or u can make a new subclass from TyperCmd and add your own necessary initializing code