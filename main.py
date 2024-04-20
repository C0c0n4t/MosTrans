# Imports
import sys

from backend.global_declarations import *
from backend.routes import *


# Main
def main(argc: int, argv: List[str]):
    db_init()

    from backend.application import run
    run()


if __name__ == '__main__':
    main(len(sys.argv), sys.argv)
