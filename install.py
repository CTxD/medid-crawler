import subprocess

from sys import argv, executable
from typing import List, Dict

from source.config import readconfig, CONFIG


def getrequirements(filepath: str) -> List[str]:
    requirements: List[str] = []
    
    with open(filepath) as fp:
        for line in fp.readlines():
            line = line.strip()
            if not line or line[0] == '#':
                continue

            if line.startswith('-r'):
                dependency = line.split()[1]
                requirements.extend(getrequirements(dependency))
                continue
            
            requirements.append(line)
    return requirements


def getuninstalledrequirements(filepath: str) -> List[str]:
    return [req for req in getrequirements(filepath) if req.lower() not in getinstalledpackages()]


def getinstalledpackages() -> Dict[str, str]:
    return {
        s.decode('utf-8').split('==')[0]: s.decode('utf-8').split('==')[1] 
        for s in subprocess.check_output([executable, '-m', 'pip', 'freeze']).split()
    }


def install():
    # Check if dependencies are installed according to the ENVIRONMENT defined in the config.cfg.
    requirements: List[str] = getuninstalledrequirements(CONFIG['REQPATH'])
    for req in requirements:
        subprocess.check_output([executable, '-m', 'pip', 'install', req])


if __name__ == '__main__':
    # If we run install directly, we make sure to populate the CONFIG dict
    readconfig('config.cfg')

    install()