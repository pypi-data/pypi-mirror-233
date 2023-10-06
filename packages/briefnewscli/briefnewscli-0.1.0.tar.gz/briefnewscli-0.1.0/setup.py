#setup.py The packaging script that specifies how your CLI should be distributed.
from setuptools import setup, find_packages

setup(
    name='briefnewscli',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'typer',  # Add any other dependencies your CLI uses
        'python-decouple',
        'requests',
        'typer',
        'torch',
        'transformers'
    ],
    entry_points='''
        [console_scripts]
        briefnewscli=brief_news_cli.cli:app
    ''',
)
