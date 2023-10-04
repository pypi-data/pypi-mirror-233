"""
A file that contain all callback logic that used in command.py file.
This file also has all CLI requirements, so don't delete it. 
"""
# search/callback.py

from sefile import (
    art,
    rich,
    typer,
    colored,
    dataclass,
    os,
    pathlib,
    Progress,
    SpinnerColumn,
    TextColumn,
    __app_name__,
    __version__,
    __creator__,
    __creator_email__,
    __project_url__,
    colors,
    Bullet,
    Input,
    Panel,
    random,
    Literal,
    )
from sefile.editor import CodeEditorApp
from sefile._custom_query import CustomQuery
from sefile._create_project import CreateProject


@dataclass
class Callback:
    def __str__(self) -> str:
        return f"{self.__class__.__name__}"
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}"
    
    @staticmethod
    def _is_valid_return(items: list, value: str) -> None:
        if len(items) < 1:
            raise FileNotFoundError(f"File '{value}' not found")
        else:
            rich.print(f"Find file '{value}' [bold green]success![/bold green]")
            raise typer.Exit()
    
    @staticmethod
    def _data_progress(path: pathlib.Path, value: str, prefix_type: Literal["startswith", "endswith"]) -> None:
        all_files = None
        with Progress(
            SpinnerColumn(spinner_name="dots9"),
            TextColumn("[progress.description]{task.description}"),
            auto_refresh=True,
            transient=True,
            get_time=None,
        ) as progress:
            task = progress.add_task(f"Please wait for a moment...", total=100_000)
            if prefix_type == "startswith":
                all_files = [os.path.join(root, some_file)
                                for root, dirs, files in os.walk(path, topdown=True)
                                for some_file in filter(lambda f: f.startswith(value), files)]
            elif prefix_type == "endswith":
                all_files = [os.path.join(root, some_file)
                                for root, dirs, files in os.walk(path, topdown=True)
                                for some_file in filter(lambda f: f.endswith(value), files)]
            else:
                raise ValueError(f"Invalid prefix type: '{prefix_type}'. Accepted values 'startswith', 'endswith'")
            for f in all_files:
                if os.path.getsize(f) != 0:
                    rich.print(f)
                    progress.advance(task)
        Callback._is_valid_return(items=all_files, value=value)

    @staticmethod
    def _create_project(choice: str) -> None:
        # input project name
        project_name = Input(f"What's the name of the {choice} project? ", word_color=colors.foreground["yellow"])
        project_name_result = project_name.launch()
        if project_name_result.find("quit") != -1 or project_name_result.find("exit") != -1:
            print("See ya! 👋")
            raise typer.Exit()
        # input project directory
        project_dir = Input(f"Where do you want to save this {project_name_result}? ", word_color=colors.foreground["yellow"])
        project_dir_result = project_dir.launch()
        if project_dir_result.find("quit") != -1 or project_dir_result.find("exit") != -1:
            print("See ya! 👋")
            raise typer.Exit()
        # check if project dir exists in your PC
        if not pathlib.Path(project_dir_result).is_dir():
            raise FileNotFoundError(f"File or Path not found, path: '{project_dir_result}'")
        else:    
            project_path = os.path.join(project_dir_result, project_name_result)
        
        if os.path.exists(project_path):
            raise FileExistsError(f"Folder exists: '{project_path}'")
        else:
            if choice.find("Python") != -1:
                _python_project = CreateProject(dir_path=project_path)
                _python_project._py_project()
            elif choice.find("Javascript") != -1:
                _javascript_project = CreateProject(dir_path=project_path)
                _javascript_project._js_project()
            elif choice.find("Go") != -1:
                _golang_project = CreateProject(dir_path=project_path)
                _golang_project._go_project()
            else:
                pass

    @staticmethod
    def _lazy_controller(user_input: str) -> None:
        if (user_input.find("quit") != -1 or 
            user_input.find("exit") != -1):
            print("See ya! 👋")
            raise typer.Exit()
        _queries = CustomQuery(command_input=user_input)
        if len(user_input.split()) == 4:
            _queries.simple_command()
        if len(user_input.split()) == 5:
            _queries.advance_command()

    def version_callback(self, value: bool) -> None:
        if value:
            selected_font_arts = ["swampland", "tarty1", "rounded", "larry3d", "henry3d", "big"]
            ascii_art = art.text2art("SEFILE", font=random.choice(selected_font_arts), chr_ignore=True)
            print(f"{colored(ascii_art, color='light_green', attrs=['bold'])}")
            rich.print(Panel(f"""[bold cyan]App name[/bold cyan]: {__app_name__}\
                    \n[bold cyan]version[/bold cyan]: [white]{__version__}[/white]\
                    \n[bold cyan]Creator name[/bold cyan]: {__creator__}\
                    \n[bold cyan]Creator email[/bold cyan]: {__creator_email__}\
                    \n[bold cyan]Creator github[/bold cyan]: [white]{__project_url__}[/white]\
                    """, 
                    title="Information", 
                    title_align="left", 
                    expand=True, 
                    highlight=True,
                    padding=(0, 1)))
            raise typer.Exit()
    
    def auto_create_callback(self, value: bool) -> None:
        if value:
            some_cli = Bullet(
                "What's project you want to create? ", 
                choices=["🐍 Easy Python", "👑 The king of Javascript", "🐼 Cute Go", "❌ Nah, i'm good"],
                bullet=" >",
                margin=2,
                bullet_color=colors.bright(colors.foreground["cyan"]),
                background_color=colors.background["default"],
                background_on_switch=colors.background["default"],
                word_color=colors.foreground["white"],
                word_on_switch=colors.foreground["white"],
                )
            result = some_cli.launch()

            if result == "🐍 Easy Python":
                Callback._create_project(choice=result)
            elif result == "👑 The king of Javascript":
                Callback._create_project(choice=result)
            elif result == "🐼 Cute Go":
                Callback._create_project(choice=result)
            else:
                print("See ya! 👋")
                raise typer.Exit()
    
    def auto_write_callback(self, value: bool) -> None:
        if value:
            code_editor_app = CodeEditorApp()
            code_editor_app.run()
            raise typer.Exit()

    def lazy_search(self, value: bool) -> None:
        if value:
            content = """[bold yellow]There are several input command you can do[/bold yellow]:\
            \n
1. find <filename> from <path>
[bold]for Linux OS[/bold]: find main.py from /home/(user)/Documents
[bold]for Windows OS[/bold]: find main.py from C:\Directory\SubDirectory
\n
2. find from <path> startswith <prefix>
[bold]for Linux OS[/bold]: find file from /home/(user)/Documents startswith main
[bold]for Windows OS[/bold]: find file from C:\Directory\SubDirectory startswith main
\n
3. find from <path> like <prefix>
[bold]for Linux OS[/bold]: find file from /home/(user)/Documents like test
[bold]for Windows OS[/bold]: find file from C:\Directory\SubDirectory like test
\n
4. quit or exit
[bold]Note[/bold]: It's can be used for all OS.
            """
            rich.print(Panel(content, title="Guide Information"))
            user_input = Input(f"Command 😃> ", word_color=colors.foreground["yellow"])
            user_input_result = user_input.launch()
            Callback._lazy_controller(user_input=user_input_result)
    
    def startswith_search(self, value: str) -> None:
        if value:
            dir_start = Input(f"From where do you want to find '{value}' file? ", word_color=colors.foreground["yellow"])
            dir_start_result = dir_start.launch()
            if dir_start_result.find("quit") != -1 or dir_start_result.find("exit") != -1:
                print("See ya! 👋")
                raise typer.Exit()
            if not pathlib.Path(dir_start_result).is_dir():
                raise FileNotFoundError(f"File or Path not found, path: '{dir_start_result}'")
            else:
                Callback._data_progress(path=dir_start_result, value=value, prefix_type="startswith")
    
    def endswith_search(self, value: str) -> None:
        if value:
            dir_start = Input(f"From where do you want to find '{value}' file? ", word_color=colors.foreground["yellow"])
            dir_start_result = dir_start.launch()
            if dir_start_result.find("quit") != -1 or dir_start_result.find("exit") != -1:
                print("See ya! 👋")
                raise typer.Exit()
            if not pathlib.Path(dir_start_result).is_dir():
                raise FileNotFoundError(f"File or Path not found, path: '{dir_start_result}'")
            else:
                Callback._data_progress(path=dir_start_result, value=value, prefix_type="endswith")

