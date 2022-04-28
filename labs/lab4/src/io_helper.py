import argparse
import os
import csv
import helper

def open_file(filename, mode = 'r'):
    try:
        file = open(filename, mode)
        return file
    except FileNotFoundError:
        print_func(f'The file {filename} was not found. Exiting from the program')
        exit(0)

def static_vars(**kwargs):
    def decorate(func):
        for k, val in kwargs.items():
            setattr(func, k, val)
        return func
    return decorate

@static_vars(outfile = None)
def print_func(message, end = '\n', init = None):
    if print_func.outfile is None and init is not None:
        assert(type(init) == str)
        print_func.outfile = open_file(init, 'w')
    if print_func.outfile is not None:
        print_func.outfile.write(message + end)
    else:
        print(message, end = end)

class writeAction(argparse.Action):
    '''
        This class makes the -w input assume "output.log" as the string input if no file name follows -w in the commandline.   

        For example:

        ```python3 learn -w output2.log [rest of the commands]```
        
        The above command will store "output2.log" in args.w

        ```python3 learn.py -w [rest of the commands]```

        The above command will store "output.log" in args.w. Make sure not to throw the input-file-path positional argument right after -w if you don't want the compiler to assume the output file as the input file given and throw an error that input-file-path positional argument not given.
    '''
    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        super().__init__(option_strings, dest, nargs = nargs, **kwargs)
    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, values) if values is not None else setattr(namespace, self.dest, "output.log")

def parse_args(args = None):
    parser = argparse.ArgumentParser(description = "CSCI-GA.2560 Artificial Intelligence Lab 4 Supervised Machine Learning: kNN and Naive Bayes")
    parser.add_argument('-train', required = True, type = str,\
        help = "something") # TODO: Write this
    parser.add_argument('-test', required = True, type = str,\
        help = "something else") # TODO: Write this too
    parser.add_argument('-K', type = int, required = False, default = 0,\
        help = "Come on! Write something") #TODO: this too
    parser.add_argument('-C', type = int, required = False, default = 0,\
        help = "blahhhhhhhhh!") # TODO: BLAHHHHHHHHHH
    parser.add_argument('-v', required = False, action = 'store_true',\
        help = 'use this tag to enable verbose output')
    parser.add_argument("-w", required = False, type = str, nargs='?', action = writeAction,\
        help = "use this tag to write the output to file called 'output.log' in the same directory")
    parser.add_argument("-debug", required = False, action = 'store_true',\
        help = "use this tag to enable debug mode")
    return parser.parse_args()


def print_args(args):
    print_func(f"-train: {args.train}")
    print_func(f"-test: {args.test}")
    print_func(f"training file: {helper.CONSTANTS.TRAIN}")
    print_func(f"testing file: {helper.CONSTANTS.TEST}")
    print_func(f"-K: {args.K}")
    print_func(f"-C: {args.C}")
    print_func(f"algo: {helper.CONSTANTS.ALGO.name}")
    print_func(f"-w: {args.w}")
    print_func(f"-debug: {args.debug}")

def assert_proper_inputs():
    if helper.CONSTANTS.K > 0 and helper.CONSTANTS.C > 0:
        print_func("K and C both cannot be greater than zero. Exiting...")
        exit(0)
    assert helper.CONSTANTS.ALGO is not None, 'algorithm should have been initialized with either naive bayes or kNN'
    if helper.CONSTANTS.TRAIN is None or os.path.splitext(helper.CONSTANTS.TRAIN)[1] != '.csv':
        print_func("training file must have extension '.csv'. Exiting...")
        exit(0)
    if helper.CONSTANTS.TEST is not None and os.path.splitext(helper.CONSTANTS.TEST)[1] != '.csv':
        print_func("training file must have the extension '.csv'. Exiting...")
        exit(0)

def csv_read(file):
    file = open_file(file)
    file_val = csv.reader(file)
    file_val = list(file_val)
    file.close()
    return file_val

def init(args):
    print_func("", "", args.w)
    helper.CONSTANTS(args.K, args.C, args.train, args.test, args.debug, (helper.ALGORITHM.NAIVE_BAYES if args.K == 0 else helper.ALGORITHM.kNN))
    assert_proper_inputs()
    if helper.CONSTANTS.DEBUG_MODE:
        print_args(args)
    helper.CONSTANTS.TRAIN = csv_read(helper.CONSTANTS.TRAIN)
    helper.CONSTANTS.TEST = csv_read(helper.CONSTANTS.TEST)
    