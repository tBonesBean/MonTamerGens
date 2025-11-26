import pathlib

from setuptools import setup, find_packages

here = pathlib.Path(__file__).parent.resolve()

setup(
    name='MonsterGenerators',
    version='0.2.0',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    package_data={
        'mongens': ['data/*'],
    },
    install_requires=[
        'setuptools==80.9.0',
        'build==1.3.0',
        'wheel==0.38.4',
        'pyproject_hooks==1.2.0',
        'pytest==9.0.1',
        'packaging==25.0',
        'astroid==4.0.2',
        'certifi==2025.11.12',
        'charset-normalizer==3.4.4',
        'colorama==0.4.6',
        'dill==0.4.0',
        'docstringify==1.1.1',
        'docutils==0.22.3',
        'id==1.5.0',
        'idna==3.11',
        'iniconfig==2.3.0',
        'isort==7.0.0',
        'jaraco.classes==3.4.0',
        'jaraco.context==6.0.1',
        'jaraco.functools==4.3.0',
        'keyring==25.7.0',
        'markdown-it-py==4.0',
        'mccabe==0.7.0',
        'mdurl==0.1.2',
        'more-itertools==10.8.0',
        'nh3==0.3.2',
        'platformdirs==4.5.0',
        'pluggy==1.6.0',
        'Pygments==2.19.2',
        'pylint==4.0.3',
    ],
    entry_points={
        'console_scripts': [
            'mongen=mongens.cli:main',
        ],
    },
    author='Your Name',
    author_email='your.email@example.com',
    description='A fantasy monster generator.',
    long_description=open('README.MD').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/monstergenerators',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
)
