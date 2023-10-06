from setuptools import setup, find_packages

classifiers = ['Development Status :: 2 - Pre-Alpha', 
               'Intended Audience :: Developers', 
               'Operating System :: MacOS :: MacOS X',
               'Operating System :: Microsoft :: Windows', 
               'Operating System :: Unix',  
               'License :: OSI Approved :: MIT License', 
               'Programming Language :: Python',]

setup(
    name= 'neurum-db',
    version='0.1.8',
    description='a simple powerful python database built on notion powered by Neurum.',
    url='',
    author='Vansh Shah',
    author_email='vanshshah836@gmail.com',
    License='MIT',
    classifiers=classifiers, 
    keywords='python notion database db free spreadsheet backend',
    packages=find_packages(),
    install_requires=[],
)