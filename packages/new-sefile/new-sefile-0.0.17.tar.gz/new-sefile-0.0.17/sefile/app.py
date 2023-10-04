# sefile/app.py

from sefile import (
    __app_name__, 
    command,
    )


def main() -> None:
    command.app(prog_name=__app_name__)

if __name__ == "__main__":
    main()