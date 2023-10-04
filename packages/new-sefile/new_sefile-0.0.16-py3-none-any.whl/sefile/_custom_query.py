"""
This file contain custom queries logic. 
So this is not the input logic but the backend system of the input.
The purpose of this file, is to make the logic of --lazy options more readable, and easy to use. 
"""
# sefile/_custom_query.py

from sefile import (
    dataclass,
    Progress,
    SpinnerColumn,
    TextColumn,
    rich,
    typer,
    pathlib,
    os,
    re,
    fnmatch,
    Literal,
)
from sefile.exception import InvalidFormat, InvalidFileFormat

"""
FOR BACKEND PURPOSE, DO NOT USE FOR INHERITANCE CLASS!
"""

@dataclass(frozen=True)
class CustomQuery:
    __slots__ = ("command_input")
    command_input: str

    @staticmethod
    def _is_valid_return(items: list, commands: list) -> None:
        if len(items) < 1:
               raise FileNotFoundError(f"File startswith {commands[-1]} not found")
        else:
            rich.print(f"Find file '{commands[-1]}' [bold green]success![/bold green]")
            raise typer.Exit()
    
    @staticmethod
    def _data_progress(commands: list, path: pathlib.Path, query_type: Literal["simple", "like", "startswith"]) -> None:
        all_files = None
        with Progress(
            SpinnerColumn(spinner_name="dots9"),
            TextColumn("[progress.description]{task.description}"),
            auto_refresh=True,
            transient=True,
            get_time=None
        ) as progress:
            task = progress.add_task("Please wait for a moment...", total=100_000)
            if query_type == "simple":
                all_files = [os.path.join(root, some_file)
                            for root, dirs, files in os.walk(path) 
                            for some_file in filter(lambda f: fnmatch.fnmatchcase(f, commands[1]), files)]
            elif query_type == "like":
                all_files = [os.path.join(root, some_file) 
                            for root, dirs, files in os.walk(path) 
                            for some_file in filter(lambda f: re.match(commands[-1], f), files)]
            elif query_type == "startswith":
                all_files = [os.path.join(root, some_file) 
                            for root, dirs, files in os.walk(path) 
                            for some_file in filter(lambda f: f.startswith(commands[-1]), files)]
            else:
                raise ValueError(f"Invalid query type: '{query_type}'. Accepted values 'simple', 'like', 'startswith'")
            for f in all_files:
                if os.path.getsize(f) != 0:
                    rich.print(f)
                    progress.advance(task)
        CustomQuery._is_valid_return(items=all_files, commands=commands)

    def simple_command(self) -> None:
        _MAX_SIMPLE_COMMAND = 4
        _results = [[] for _ in range(_MAX_SIMPLE_COMMAND)]
        try:
            for i, value in enumerate(self.command_input.split()):
                _results[i].append(value)
        except:
            raise InvalidFormat(f"Invalid input format. Please use the correct format, input: '{self.command_input}'")
        
        _all_commands = [subitem for item in _results for subitem in item]
        
        if len(_all_commands) != _MAX_SIMPLE_COMMAND:
            raise InvalidFormat(f"Invalid format, input: '{self.command_input}'")

        if _all_commands[0] != "find" or _all_commands[2] != "from":
            raise InvalidFormat(f"Invalid format, input: '{self.command_input}'")

        if _all_commands[1].find(".") == -1:
            raise InvalidFileFormat(f"Invalid file format, file: '{_all_commands[-3]}'")

        if (curr_path := pathlib.Path(_all_commands[-1])) and not curr_path.is_dir():
            raise FileNotFoundError(f"Directory '{_all_commands[-1]}' not found.")

        CustomQuery._data_progress(commands=_all_commands, path=curr_path, query_type="simple")
    
    def advance_command(self) -> None:
        _MAX_ADVANCE_COMMAND = 5
        _results = [[] for _ in range(_MAX_ADVANCE_COMMAND)]
        try:
            for i, value in enumerate(self.command_input.split()):
                _results[i].append(value)
        except:
            raise InvalidFormat(f"Invalid input format. Please use the correct format, input: '{self.command_input}'")
        
        _all_commands = [subitem for item in _results for subitem in item]
        
        if len(_all_commands) != _MAX_ADVANCE_COMMAND:
                raise InvalidFormat(f"Invalid format, input: '{self.command_input}'")
        
        if (_all_commands[0] != 'find' or _all_commands[1] != 'from'):
            raise InvalidFormat(f"Invalid format, input: '{self.command_input}'")

        if (curr_path := pathlib.Path(_all_commands[2])) and not curr_path.is_dir():
                raise FileNotFoundError(f"Directory '{_all_commands[-1]}' not found.")
        
        if _all_commands[3] != "like" and _all_commands[3] != "startswith":
            raise InvalidFormat(f"Invalid format, input: '{self.command_input}'")
        
        if _all_commands[3] == "like":
            CustomQuery._data_progress(commands=_all_commands, path=curr_path, query_type="like")
        
        if _all_commands[3] == "startswith":
            CustomQuery._data_progress(commands=_all_commands, path=curr_path, query_type="startswith")
