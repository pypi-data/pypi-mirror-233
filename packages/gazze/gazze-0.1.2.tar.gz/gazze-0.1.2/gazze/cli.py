import time
import click

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def title(text: str):
    return f'{bcolors.OKCYAN}gazze-cli{bcolors.ENDC} {text}'

def byell(text: str):
    return f'{bcolors.WARNING}{bcolors.BOLD}{text}{bcolors.ENDC}{bcolors.ENDC}'

def bgree(text: str):
    return f'{bcolors.OKGREEN}{bcolors.BOLD}{text}{bcolors.ENDC}{bcolors.ENDC}'

@click.group()
def main(): pass