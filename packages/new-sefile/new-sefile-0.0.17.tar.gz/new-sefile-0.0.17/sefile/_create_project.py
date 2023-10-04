"""
This file contain backend system of creating project from create command.
Every folder and file that automatically created by the system it's build on top of list comprehension,
which make the create system more faster instead of using flat list.
"""
# sefile/_create_project.py

from sefile import (
    dataclass,
    os,
    rich,
)


@dataclass(frozen=True)
class CreateProject:
    __slots__ = ("dir_path")
    dir_path: str

    def __str__(self) -> None:
        return f"({self.dir_path})"
    
    def __repr__(self) -> None:
        return f"{self.__class__.__name__}({self.dir_path})"

    def _py_project(self) -> None:
        os.mkdir(self.dir_path)
        # create sub directory
        [os.makedirs(os.path.join(self.dir_path, subdir)) 
         for subdir in ["src", "tests"]]
        # create files in sub directory
        [open(os.path.join(os.path.join(self.dir_path, "src"), src_file), 'x') 
         for src_file in ["__init__.py", "main.py"]]
        # create files in sub directory
        [open(os.path.join(os.path.join(self.dir_path, "tests"), tests_file), 'x') 
         for tests_file in ["__init__.py", "test.py"]]
        # create required files for deployment
        [open(os.path.join(self.dir_path, req_file), 'x') 
         for req_file in ["LICENSE.md", "README.md", "requirements.txt"]]
        rich.print(f"All [bold green]Done![/bold green] ✅, path: '{self.dir_path}'")
    
    def _js_project(self) -> None:
        os.mkdir(self.dir_path)
        # create sub directory
        [os.makedirs(os.path.join(self.dir_path, subdir)) 
         for subdir in ["src", "tests", "public"]]
        # create files in sub directory
        [open(os.path.join(os.path.join(self.dir_path, "src"), src_file), "x") 
         for src_file in ["index.js", "app.js"]]
        # create files in sub directory
        [open(os.path.join(os.path.join(self.dir_path, "public"), public_file), "x") 
         for public_file in ["index.html", "style.css", "script.js"]]
        # create files in sub directory
        [open(os.path.join(os.path.join(self.dir_path, "tests"), tests_file), "x") 
         for tests_file in ["service.test.js", "component.test.js"]]
        # create required files for deployment
        [open(os.path.join(self.dir_path, req_file), "x") 
         for req_file in ["LICENSE.md", "README.md", "package.json"]]
        rich.print(f"All [bold green]Done![/bold green] ✅, path: {self.dir_path}")
    
    def _go_project(self) -> None:
        os.mkdir(self.dir_path)
        # create sub directory
        [os.makedirs(os.path.join(self.dir_path, subdir)) 
         for subdir in ["src", "tests"]]
        # create files in sub directory
        [open(os.path.join(os.path.join(self.dir_path, "src"), src_file), "x") 
         for src_file in ["main.go", "utils.go"]]
        # create files in sub directory
        [open(os.path.join(os.path.join(self.dir_path, "tests"), tests_file), "x") 
         for tests_file in ["test.go"]]
        # create required file for deployment
        [open(os.path.join(self.dir_path, req_file), "x") 
         for req_file in ["LICENSE.md", "README.md", "config.go"]]
        rich.print(f"All [bold green]Done![/bold green] ✅, path: {self.dir_path}")
