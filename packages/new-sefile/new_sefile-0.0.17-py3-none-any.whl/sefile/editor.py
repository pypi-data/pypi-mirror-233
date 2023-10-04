"""
This file contain logic for Code Editor Interface that shows up when do create -w options. 
To be honest, this program not 100 % good, because the main package of this program, 
was not updated from 2015 ago, so i think, this program could be not used in this CLI tool,
maybe in next update? we'll see.
"""
# search/npyscreen_app.py

from sefile import (
    npyscreen, 
    curses, 
    os, 
    pathlib,
    )

# test creating custom theme
class CustomTheme(npyscreen.ThemeManager):
    default_colors = {
        'DEFAULT'     : 'CYAN_BLACK',
        'FORMDEFAULT' : 'YELLOW_BLACK',
        'NO_EDIT'     : 'GREEN_BLACK',
        'STANDOUT'    : 'CYAN_BLACK',
        'CURSOR'      : 'WHITE_BLACK',
        'CURSOR_INVERSE': 'BLACK_WHITE',
        'LABEL'       : 'GREEN_BLACK',
        'LABELBOLD'   : 'WHITE_BLACK',
        'CONTROL'     : 'GREEN_BLACK',
        'IMPORTANT'   : 'GREEN_BLACK',
        'SAFE'        : 'GREEN_BLACK',
        'WARNING'     : 'YELLOW_BLACK',
        'DANGER'      : 'RED_BLACK',
        'CRITICAL'    : 'BLACK_RED',
        'GOOD'        : 'GREEN_BLACK',
        'GOODHL'      : 'GREEN_BLACK',
        'VERYGOOD'    : 'BLACK_GREEN',
        'CAUTION'     : 'YELLOW_BLACK',
        'CAUTIONHL'   : 'BLACK_YELLOW',
    }

# define our action form
class CodeEditor(npyscreen.ActionFormV2):
    # define custom button text
    OK_BUTTON_TEXT = "SAVE"
    CANCEL_BUTTON_TEXT = "EXIT"

    def activate(self):
        self.edit()
        self.parentApp.setNextForm(None)

    def draw_title_and_help(self):
        if self.name:
            title = self.name[:(self.columns-4)]
            title = ' ' + str(title) + ' '
            if isinstance(title, bytes):
                title = title.decode('utf-8', 'replace')
            self.add_line(0,58, 
                title, 
                self.make_attributes_list(title, curses.A_BOLD),
                self.columns-4
                )

    def create(self):
        self.filename = self.add(
            npyscreen.TitleFilename,
            begin_entry_at=18,
            name="Filename      :",
            relx=3,
            rely=2,
            )
        self.path = self.add(
            npyscreen.TitleText,
            begin_entry_at=18,
            name="Folder Path   :",
            relx=3, 
            rely=4,
            editable=True
            )
        self.code = self.add(
            npyscreen.MultiLineEdit,
            relx=2, 
            rely=6,
            editable=True,
            scroll_exit=True,
            )
    
    # add method for condition where user pick 'SAVE' button
    def on_ok(self):
        # raise error if filename not include file type
        if self.filename.value.find(".") == -1:
            raise ValueError(f"'filename' needs file type at the end, file: {self.filename.value}")
        
        if not self.path.value:
            raise ValueError(f"Path is required, path: '{self.path.value}'")
        
        # define path
        curr_path = pathlib.Path(self.path.value)
        if curr_path.is_dir():
            real_path = os.path.join(curr_path, self.filename.value)
            if os.path.exists(real_path):
                raise FileExistsError(f"File exists: {real_path}")
            else:
                if self.filename.value.endswith('.txt'):
                    with open(os.path.join(self.path.value, self.filename.value), "a+") as file:
                        file.seek(0)
                        is_content_exist = file.read()

                        if is_content_exist:
                            file.write("\n"+self.code.value)
                        else:
                            file.write(self.code.value)
                        file.close()
                else:
                    with open(os.path.join(self.path.value, self.filename.value), 'a+') as file:
                        file.seek(0)
                        is_code_exist = file.read()
                        
                        if is_code_exist:
                            file.write("\n\n"+self.code.value)
                        else:
                            file.write(f"# {self.filename.value}\n\n"+self.code.value)
                        file.close()
        
# write your custom code editor here 
class CodeEditorApp(npyscreen.NPSAppManaged):
    def onStart(self):
        self.appTheme = npyscreen.setTheme(CustomTheme)
        self.addForm("MAIN", CodeEditor, name="Code Editor V1")

