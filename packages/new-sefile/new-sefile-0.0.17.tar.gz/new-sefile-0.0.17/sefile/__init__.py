"""Top-Level package for search file"""
# search_app/__init__.py

import functools
import art
import fnmatch
import inspect
import logging
import npyscreen
import curses
import os
import shutil
import stat
import pathlib
import platform
import rich
import re
import time
import typer
import random
import subprocess
import sys
import warnings
from bullet import (
    colors,
    Bullet, 
    VerticalPrompt,
    SlidePrompt,
    Input,
    )
from colorama import (
    Fore, 
    Back, 
    Style
    )
from dataclasses import dataclass
from enum import Enum
from termcolor import colored
from typing import (
    Optional, 
    Union,
    Literal,
    )
from rich.console import Console, Group
from rich.panel import Panel
from rich.progress import (
    Progress, 
    SpinnerColumn, 
    TextColumn
    )
from rich.syntax import Syntax
from rich.layout import Layout


# throw all information about this CLI below
__app_name__ = "Sefile CLI Tool"
__version__ = "0.0.17"
__creator__ = "Faisal Ramadhan"
__creator_email__ = "faisalramadhan1299@gmail.com"
__project_url__ = "https://github.com/kolong-meja"
