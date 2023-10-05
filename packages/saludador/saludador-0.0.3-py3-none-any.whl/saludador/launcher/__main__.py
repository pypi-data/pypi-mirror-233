import sys
# from saludador.modules.examples import saluda
import saludador.modules.examples as saludador



from rich import print
from saludador.launcher.__version__ import __VERSION__


def main():
    print(f"[[bold green]Hola mundo python[/]] version {__VERSION__}")
    print("probando el modulo salduador: ", saludador.saluda())
if __name__ == "__main__":
    sys.exit(main())
