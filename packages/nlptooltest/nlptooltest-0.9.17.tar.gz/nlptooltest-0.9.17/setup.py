#!/usr/bin/env python

"""The setup script."""
import os 
from setuptools import setup, find_packages
VERSION_FILE = os.path.join(os.path.dirname(__file__),
                            'nlptools',
                            'VERSION')
with open(VERSION_FILE, encoding='utf-8') as version_fp:
    VERSION = version_fp.read().strip()
with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'six',
    'farasapy',
    'tqdm',
    'requests',
    'regex',
    'pathlib',
    'torch==1.13.0',
    'transformers==4.24.0',
    'torchtext==0.14.0',
    'torchvision==0.14.0',
    'seqeval==1.2.2',
    'natsort==7.1.1'
]

test_requirements = [ ]

# setup(
    # author="Sina Institute",
    # author_email='sina.institute.bzu@gmail.com',
    # python_requires='>=3.6',
    # classifiers=[
        # 'Development Status :: 2 - Pre-Alpha',
        # 'Intended Audience :: Developers',
        # 'License :: OSI Approved :: MIT License',
        # 'Natural Language :: English',
        # 'Programming Language :: Python :: 3',
        # 'Programming Language :: Python :: 3.6',
        # 'Programming Language :: Python :: 3.7',
        # 'Programming Language :: Python :: 3.8',
        # 'Programming Language :: Python :: 3.9',
        # 'Programming Language :: Python :: 3.10',
    # ],
    # description="Python Boilerplate contains all the boilerplate you need to create a Python package.",
    # entry_points={
        # 'console_scripts': [
            # 'nlptools=nlptools.cli:main',
        # ],
    # },
    # package_data={'nlptools': ['data/*.pickle']},
    # install_requires=requirements,
    # license="MIT license",
    # long_description=readme + '\n\n' + history,
    # include_package_data=True,
    # keywords='nlptools',
    # name='nlptooltest',
    # packages=find_packages(include=['nlptools', 'nlptools.*']),
    # test_suite='tests',
    # tests_require=test_requirements,
    # url='https://github.com/SinaLab/nlptools',
    # version=VERSION,
    # zip_safe=False,
# )


setup(
    entry_points={
        'console_scripts': [
            'sina_arStrip = nlptooltest.CLI.utils.arStrip:main',
            'sina_jaccard_similarity = nlptooltest.CLI.utils.jaccard_similarity:main',
            'sina_implication = nlptooltest.CLI.utils.implication:main',
            'sina_corpus_tokenizer = nlptooltest.CLI.utils.corpus_tokenizer:main',
        ],                                                                                                                                                                                                           
    },
    package_data={'nlptools': ['data/*.pickle']},
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='nlptools, CLI',
    name='nlptooltest',
    packages=find_packages(include=['nlptools', 'nlptools.*', 'CLI', 'CLI.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/SinaLab/nlptools',
    version=VERSION,
    zip_safe=False,
)