from setuptools import setup, find_packages

setup(
    name="Torrscrape",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "requests",
        "qbittorrent-api",
        "pandas",
        "tabulate",
        "click",        
    ],
    entry_points={
        "console_scripts": [
            "torrscrape=Torrscrape.main:main",
        ],
    },
)
