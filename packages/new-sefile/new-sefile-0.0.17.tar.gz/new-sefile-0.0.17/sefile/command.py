# search_app/command.py

from sefile import (
    pathlib, 
    typer, 
    Optional,
    )
from sefile.controllers import Controller
from sefile.callbacks import Callback
from sefile.config import (
    app, 
    FileTypes,
    ThemeSelection,
    )


@app.command(help="Command to [bold yellow]find[/bold yellow] files from <path> 🔍.")
def find(filename: str = typer.Argument(help="Name of file to [bold yellow]search[/bold yellow] for. :page_facing_up:", 
                                        metavar="FILENAME"),
        path: str = typer.Argument(metavar="PATH", 
                                   help="Directory path for the file to search."),
        startswith: str = typer.Option(None, "--startswith", "-s", 
                                        help="Search specific file with 'startswith' method :rocket:.", 
                                        is_eager=True, 
                                        callback=Callback.startswith_search), 
        endswith: str = typer.Option(None, "--endswith", "-e", 
                                    help="""Search specific file with 
                                    'endswith' method :sunrise_over_mountains:""", 
                                    is_eager=True, 
                                    callback=Callback.endswith_search),
        lazy: Optional[bool] = typer.Option(None, "--lazy", "-l",
                                            help=f"Input a special query if you are too lazy to type using CLI commands", 
                                            is_eager=True, 
                                            callback=Callback.lazy_search)) -> None:
    """
    TODO: Define find logic from controllers
    """
    find_logic = Controller(filename=filename, path=path)
    find_logic.find_controller(startswith=startswith, endswith=endswith, lazy=lazy)

@app.command(help="Command to [bold green]create[/bold green] new file in <path>:cookie:.")
def create(filename: str = typer.Argument(default=None, metavar="FILENAME", 
                                          help="Name of file to [bold green]create[/bold green] a new one. :page_facing_up:"),
           path: str = typer.Argument(default=None, metavar="PATH", 
                                      help="Directory [bold blue]path[/bold blue] for file that has been created. :file_folder:"),
           project: Optional[bool] = typer.Option(None, "--project", "-p", 
                                               help="Automatically create simple (Python, Javascript, and Go).", 
                                               is_eager=True,
                                               callback=Callback.auto_create_callback),
           write: Optional[bool] = typer.Option(None, "--write", "-w", 
                                                help="Create and write a file in one time.", 
                                                is_eager=True, 
                                                callback=Callback.auto_write_callback)) -> None:
    """
    TODO: Define create logic from controllers
    """
    create_logic = Controller(filename=filename, path=path)
    create_logic.create_controller(project=project, write=write)

@app.command(help="Command to [bold]read[/bold] file from <path> :book:.")
def read(filename: str = typer.Argument(metavar="FILENAME", 
                                        help="Name of file to read of. :page_facing_up:"),
        path: str = typer.Argument(metavar="PATH", 
                                   help="Directory path of file that want to read of. :file_folder:"),
        format: FileTypes = typer.Option(FileTypes.text.value, "--format", "-f", 
                                        is_flag=True, 
                                        help="Read files according to file format. :computer:"),
        indent: bool = typer.Option(False, "--indent", "-i", 
                                    is_flag=True, 
                                    help="Display indent guides to the code."),
        theme: ThemeSelection = typer.Option(ThemeSelection.dark.value, "--theme", "-t", 
                                            is_flag=True, 
                                            help="Display code with selection theme.")) -> None:
    """
    TODO: Define read logic from controllers
    """
    read_logic = Controller(filename=filename, path=path)
    read_logic.read_controller(format=format, indent=indent, theme=theme)

@app.command(help="Command to [bold red]remove[/bold red] a file from <path> :eyes:.")
def remove(path: Optional[str] = typer.Argument(default=None, 
                                                metavar="PATH", 
                                                help="Directory of file to be deleted. :file_folder:"),
            filename: Optional[str] = typer.Argument(default=None, 
                                                    metavar="FILENAME", 
                                                    help="Name of file to be removed. :page_facing_up:"),
            startswith: str = typer.Option(None, "--startswith", "-s", 
                                          is_flag=True, 
                                          help="Remove certain file startswith <prefix>",
                                          callback=None),
            endswith: str = typer.Option(None, "--endswith", "-e", 
                                        is_flag=True, 
                                        help="Remove certain file endswith <prefix>.",
                                        callback=None),
            subfolder: bool = typer.Option(False, "--subfolder", "-sf", 
                                                    is_flag=True,
                                                    help="Remove subfolder and it's content from <path>.")) -> None:
    """
    TODO: Define write logic from controllers
    """
    delete_logic = Controller(filename=filename, path=path)
    delete_logic.delete_controller(startswith=startswith, endswith=endswith, subfolder=subfolder)

# main function in here!
@app.callback()
def main(info: Optional[bool] = typer.Option(None, "--info", "-i", 
                                                help="Show version and information of this CLI tool.", 
                                                is_eager=True, 
                                                callback=Callback.version_callback)) -> None: return
