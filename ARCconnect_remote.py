# -*- coding: utf-8 -*-
"""
Cornell Aerial Robotics Club

This script is inteneded to run on start up on ARC's Raspberrypis. It will
retrieve the internal IP adress of the pi, and email it, along with the name of
the pi, to arc.pi.reg@gmail.com.

The script piconnectlocal.py retrieves the information from this email and
starts and SSH session with this Raspberry pi.

Arguments:
    pwd    Password for arc.pi.reg@gmail.com

date: 2019-11-08
author: Eric Jackson
email: ebj29-at-cornell-dot-edu
"""
import argparse
import socket
import smtplib
import ssl
import time


def main():
    parser = argparse.ArgumentParser(description=""" This script is inteneded
                                     to run on start up on ARC's Raspberrypis.
                                     It will retrieve the internal IP adress of
                                     the pi, and email it, along with the name
                                     of the pi, to arc.pi.reg@gmail.com.""")

    parser.add_argument('pwd', help='Password for arc.pi.reg@gmail.com')
    args = parser.parse_args()

    time.sleep(15)

    name = socket.gethostname()  # name of localhost
    addr = getIP()  # local IP address

    sendIP(name, args.pwd, addr)


def sendIP(name, pwd, addr):
    """
    Sends an email to arc.pi.reg@gmail.com of the format:
        <name> <local IP address>

    Parameters:
        name    Name of this raspberry pi
        pwd     Password for arc.pi.reg@gmail.com
        addr    Devices local IP address
    """
    usr = "arc.pi.reg@gmail.com"
    prt = 465

    with smtplib.SMTP_SSL('smtp.gmail.com', prt) as server:
        server.login(usr, pwd)
        server.sendmail(usr, usr, name + " " + addr)
        server.quit()


def getIP():
    """ Returns this device's local IP address. """
    conn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    conn.connect(("1.1.1.1", 1))
    addr = conn.getsockname()[0]
    conn.close()
    return addr


if __name__ == '__main__':
    main()
