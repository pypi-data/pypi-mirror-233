from setuptools import setup, find_packages
import pathlib
here = pathlib.Path(__file__).parent.resolve()

setup(
    name='PyGitLinguist',
    version='1.0.1',
    description='Python version of github\'s Linguist',
    author='Guy Nachshon',
    author_email='guy.na8@gmail.com',
    url='https://github.com/guy-nachshon/pylinguist',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    python_requires='>=3.7, <4'
)