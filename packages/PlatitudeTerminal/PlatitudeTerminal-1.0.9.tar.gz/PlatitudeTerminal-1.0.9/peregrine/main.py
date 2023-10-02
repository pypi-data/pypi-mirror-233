from peregrine import cli
import warnings
from requests.exceptions import RequestsDependencyWarning


def main():
    warnings.simplefilter('ignore', RequestsDependencyWarning)
    cli.app()

if __name__ == "main":
    warnings.simplefilter('ignore', RequestsDependencyWarning)
    main()