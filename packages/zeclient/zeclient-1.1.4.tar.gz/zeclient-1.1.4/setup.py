'''
Created on May 8, 2019
Updated on April 12, 2022

@author: ZE
'''

from distutils.core import setup

test_dependencies = [
        'pytest-cov',
        'pytest',
        'configparser',
        'numpy',
        'tabulate',
        'validate_email'
]

setup(
    name='zeclient',
    version='1.1.4',
    author='ZE',
    author_email='support@ze.com',
    packages=['zeclient', 'zeclient.oauth2'],
    url='http://www.ze.com',
    license='LICENSE.txt',
    description='Python APIs for ZE Web Services.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    python_requires='>=3.5',
    install_requires=[
        'requests',
        'lxml',
        'dicttoxml',
        'pandas',
        'zeep',
        'beautifulsoup4'
    ],
    tests_require=test_dependencies,
    extras_require={'test': test_dependencies}
)
