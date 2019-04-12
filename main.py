import logging
import os
import sys
import socket

from typing import Union

from source import config, medid
from install import getuninstalledrequirements, install


# The logger is configured in source/__init__.py, so make sure to import something from source
# before getting a logger instance. This way we use that configuration instead of creating a new,
# default configuration. Also, the name of the logger must be 'source' (instead of __name__) when
# getting a logger instance here, as it will manipulate the logger to believe this file is part of
# the source module (which it is not!). In all other places __name__ should still be used when
# getting logger instances!
logger = logging.getLogger('source')


def main():
    if '-I' in sys.argv:
        install()

    if not resolvedependencies():
        exit()
    print('Everything OK!\r\n')

    logger.info('Starting application.')

    # Start the crawling process
    medid.crawlloop()


def checkrequirements() -> bool:
    # Are all requirements installed?
    printstatus('Checking requirements')
    res = getuninstalledrequirements(config.CONFIG['REQPATH'])

    status = False if res else True
    printstatus(status)

    if not status:
        print(
            f'\r\nThe following package{"s" if len(res) > 1 else ""} needs to be installed:')
        for req in res:
            print(' - ' + req)
        print(
            'Run one of the following commands to resolve dependencies:\r\n'
            f'\tpip install -r {config.CONFIG["REQPATH"]}\r\n'
            f'\tpython main.py -I'
        )

    return status


def checkconnection() -> bool:
    # Connectivity check implementation is heavily inspired by the following SO answer:
    # https://stackoverflow.com/a/33117579

    printstatus('Checking internet connection')
    status = True
    try:
      socket.setdefaulttimeout(5)
      socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect(("8.8.8.8", 53))
    except Exception:
        status = False

    printstatus(status)
    return status


def checkcertificate() -> bool:
    from source.config import CONFIG
    # Access to DB instance?
    printstatus('Checking Firebase certificate')

    certificate_path = 'CERT' in CONFIG
    if not certificate_path:
        printstatus(False)
        print(
            f'\r\nNo CERT path has been defined in the config.cfg file. Please make sure a CERT '
            'entry exists, either globally or for the current environment.'
        )
        return False
    
    certpath = os.path.join(os.getcwd(), CONFIG["CERT"])
    certificate_exists = os.path.exists(certpath)
    if not certificate_exists:
        printstatus(False)
        print(
            f'\r\nNo certificate exists in the path "{certpath}". Make sure the path to the '
            'certificate is valid.'
        )
        return False
    
    try:
        from firebase_admin import credentials
        credentials.Certificate(certpath)
    except ImportError:
        printstatus(False)
        print(
            f'\r\nCould not import firebase_admin package. This is unexpected; please install the '
            f'package manually with command: \r\n\tpip3 install --force-reinstall firebase-admin'
        )
        return False
    except ValueError:
        printstatus(False)
        print(f'\r\nThe certificate at {certpath} is not a valid Firebase certificate.')
        return False
    except Exception:
        printstatus(False)
        print('Unexpected failure in resolving the certificate dependency.')
        return False

    printstatus(True)

    return True


def checkconfig() -> bool:
    printstatus('Checking config file')
    status = True
    extra = ''

    # Does a file named config.cfg exist?
    if not os.path.exists(os.path.join(os.getcwd(), 'config.cfg')):
        status = False
        extra = '\r\nNo config.cfg file exists or it is misplaced. Make sure the config.cfg file '\
                f'is located in the {os.getcwd()} directory.'
        # If a config.cfg.example file exists, inform the user to use that.
        if os.path.exists(os.path.join(os.getcwd(), 'config.cfg.example')):
            extra = extra + '\r\nA template config.cfg file exists. Make a copy of ' \
                'config.cfg.example template file, renaming it config.cfg.'

    printstatus(status)

    if extra:
        print(extra)

    return status


def resolvedependencies() -> bool:
    if not checkconfig():
        return False

    config.readconfig('config.cfg')

    if not checkrequirements() or not checkconnection() or not checkcertificate():
        return False

    return True


def printstatus(status: Union[str, bool]):
    message = ''
    if isinstance(status, str):
        message = "{:<40}".format(status+'...')
    else:
        message = "\033[92m OK!\033[00m" if status is True else "\033[91m Failed\033[00m"
        message = message + '\r\n'

    sys.stdout.write(message)
    sys.stdout.flush()


if __name__ == '__main__':
    main()
