from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='PyAlStruct',
    version='0.8.0',
    author='Fathi Abdelmalek',
    author_email='abdelmalek.fathi.2001@gmail.com',
    url='https://github.com/fathiabdelmalek/PyAlStruct',
    description='Implementation of data structures and algorithms in python',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=['al_struct.algorithms',
              'al_struct.algorithms.search',
              'al_struct.algorithms.sort',
              'al_struct.data_structures',
              'al_struct.data_structures.lists',
              'al_struct.data_structures.queues',
              'al_struct.data_structures.stacks',
              'al_struct.data_structures.trees',
              'al_struct.utils',
              ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Topic :: Education",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ]
)
