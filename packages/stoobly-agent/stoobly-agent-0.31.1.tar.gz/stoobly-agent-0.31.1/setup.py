import os

from setuptools import find_packages, setup

from stoobly_agent import COMMAND, VERSION

def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join('..', path, filename))
    return paths

public_files_relative_path = 'stoobly_agent/public'
public_files = package_files(public_files_relative_path)

db_files_relative_path = 'stoobly_agent/db'
db_files = package_files(db_files_relative_path)

test_dependencies = [
    'mock',
    'pytest',
]

setup(
    author='Matt Le',
    author_email='michael@stoobly.com',
    description='Record, mock, and test HTTP(s) requests. CLI agent for Stoobly',
    entry_points={
        'console_scripts': [
            'stoobly-agent=stoobly_agent.cli:main'
        ]
    },
    extras_require={
        'test': test_dependencies,
    },
    include_package_data=True,
    install_requires=[
        "click>=7.0.0,<8.0.0",
        "distro>=1.6.0,<1.7.0",
        "httptools>=0.4.0",
        "jmespath>=1.0.0",
        "markupsafe<2.1.1", # Otherwise causes ImportError: cannot import name 'url_quote' from 'werkzeug.urls'
        "mergedeep>=1.3.0,<1.3.4",
        "mitmproxy>=8.0.0,<=8.1.0",
        "openapi-core>=0.17.0",
        "stoobly_orator>=0.9.12",
        "pyyaml>=6.0.1",
        "requests>=2.31.0",
        "tabulate>=0.8.8",
        "watchdog>=2.1.0,<=2.1.3",
        "yamale>=4.0.0,<=4.0.2"
    ],
    license='MIT',
    name=COMMAND,
    readme='README.md',
    packages=find_packages(include=[
        'stoobly_agent', 'stoobly_agent.*',
    ]),
    package_data={
        'stoobly_agent': ['config/*'] + db_files + public_files
    },
    #scripts=['bin/stoobly-agent'],
    tests_requires=test_dependencies,
    url='https://github.com/Stoobly/stoobly-agent',
    version=VERSION,
)


