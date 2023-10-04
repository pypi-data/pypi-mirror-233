import sys
from rich import print

from saludador.launcher.__version__ import __VERSION__

def main():
    print(f"[[bold green]Hola mundo python[/]] version {__VERSION__}")

if __name__ == "__main__":
    sys.exit(main())
