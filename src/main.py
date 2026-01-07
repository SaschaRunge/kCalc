from dataset import DataSet
from application import Application
from math_m import Math_m
from cli import CLI

def main():
    application = Application()
    dataset = DataSet()
    cli = CLI(dataset)
    cli.run()

if __name__ == '__main__':
    main()