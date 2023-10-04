from setuptools import setup


setup(
    name='pyappi',
    version='1.3.4',
    packages=['pyappi', 
              'tests',
              'pyappi.client',
              'pyappi.logs',
              'pyappi.block',
              'pyappi.document',
              'pyappi.encoding',
              'pyappi.stats',
              'pyappi.sync',
              'pyappi.user',
              'pyappi.util',
              'pyappi.service',
              'pyappi.events'],
    license='Copyright (c) All Rights Reserved',
    description="Native Python Appi implementation. Single threaded, single node, no plug-ins.",
    long_description=open('README.md').read(),
    entry_points={
        'console_scripts': ['pyappi=pyappi.server_cli:main',
                            'pyappi-client=pyappi.client_cli:main'
                            ],
    },
    install_requires=[
        "wheel",
        "uvicorn",
        "twine",
        "fastapi",
        "pathvalidate",
        "twine",
        "colorama",
        "httpx",
        "click",
        "websockets",
        "pycryptodome"
    ],
)
