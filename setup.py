from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


AUTHER_NAME = 'Shah Khurram'
SRC_REPO = 'src'
LIST_OF_REQUIREMENTS = ['streamlit']

setup(
    name = SRC_REPO,
    version = '0.0.1',
    auther = AUTHER_NAME,
    author_email = 'khurramgaur8@gmail.com',
    description = 'A small package of movies recommander system',
    long_description = 'text/markdown',
    url = '',
    package = [SRC_REPO],
    python_requires = '>=3.11',
    install_requirements = LIST_OF_REQUIREMENTS
)




