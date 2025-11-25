from setuptools import setup, find_packages

setup(
    name='mongens',
    version='0.1.0',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    package_data={
        'mongens': ['data/*'],
    },
    install_requires=[
        # any dependencies your project needs
    ],
    entry_points={
        'console_scripts': [
            'mongen=mongens.cli:main',
        ],
    },
    author='Your Name',
    author_email='your.email@example.com',
    description='A fantasy monster generator.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/monstergenerators',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
