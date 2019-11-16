# -*- coding: utf-8 -*-
"""
Cornell Aerial Robotics Club

Starts an SSH session with one of ARC's raspberry pis.

Arguments:
    usr    Username for the remote device.
    pwd    Password for arc.pi.reg@gmail.com.

date: 2019-11-08
author: Eric Jackson
email: ebj29-at-cornell-dot-edu
"""

import argparse
import imaplib
import os


def main():
    """ Starts an SSH session with one of ARC\'s Raspberry pis. """
    parser = argparse.ArgumentParser(description="""Starts SSH session with one
                                     of ARC\'s Raspberrypis.""")

    parser.add_argument('usr', help='Username for the remote device.')
    parser.add_argument('pwd', help='Password for arc.pi.reg@gmail.com.')

    args = parser.parse_args()

    address = get_IP(IP_list(args.pwd), args.usr)
    os.system("ssh " + "pi" + "@" + address)


def IP_list(pwd):
    """ Returns an array of (pi user, internal IP) duples.  """
    # Connect to the gmail server.
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login('arc.pi.reg@gmail.com', pwd)

    # get mail IDs.
    mail.select('Inbox')
    typ, data = mail.search(None, 'ALL')
    mail_ids = data[0].decode()
    id_list = mail_ids.split()

    pi_ip = []

    # More description here.
    for id in id_list[::-1]:
        typ, msg_data = mail.fetch(id, '(BODY.PEEK[TEXT])')
        msg = msg_data[0][1].decode().strip()

        name, addr = msg.split(" ")
        pi_ip.append((name, addr))

    return pi_ip


def get_IP(lst, usr):
    """
    Returns the adress of the first element in the array with the
    username usr.
    """
    for element in lst:
        if element[0] == usr:
            return element[1]


if __name__ == '__main__':
    main()
