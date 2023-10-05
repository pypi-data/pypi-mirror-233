from setuptools import setup, find_packages

setup(
    name='PyGitLinguist',
    version='1.5.1',
    description='Pythonic version of github\'s Linguist',
    author='Guy Nachshon',
    author_email='guy.na8@gmail.com',
    url='https://github.com/guy-nachshon/pylinguist',
    packages=find_packages(),
    py_modules=["lang_detect", "pylinguist"],
    include_package_data=True,
    install_requires=[
        'chardet',
        'GitPython',
        'PyYAML',
        ],
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