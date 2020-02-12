#!/usr/bin/env python3

from time import sleep


def zero(logging):
    logging.info('zeroing environment')


def hover(logging, x, y, z):
    logging.info('hovering at ({}, {}, {})'.format(x, y, z))


def wait(logging, t):
    logging.info('waiting for {} seconds'.format(t))
    sleep(int(t))


def parse_line(tok_list):

    INSTRUCTIONS = {
        'zero':     zero,
        'hover':    hover,
        'wait':     wait,
    }

    return INSTRUCTIONS[tok_list[0]], tok_list[1:]


def parse(fp):
    ''' Parses a flight plan file into a list of instruction.

    Parameters:
    fp (string): a string of instructions separated by newlines.

    Returns:
    ((func, args list) list): 
    '''

    tokens = list(map(lambda i : i.strip().split(), fp.split('\n')))
    tokens = filter(lambda tok_list : len(tok_list) != 0, tokens)
    return list(map(parse_line, tokens))


def _test():
    pass


if __name__ == '__main__':
    _test()
