from setuptools import setup, find_packages

setup(
    name='labrinth',
    version='0.1.2',
    author='YourLocalMoon',
    author_email='kovaslavs@gmail.com',
    description='A Python API wrapper for Modrinth (labrinth because why not)',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        'requests',
    ],
)