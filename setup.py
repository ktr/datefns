"""
setuptools for datefns
"""

from setuptools import setup, find_packages
from os import path


def get_long_desc():
    here = path.abspath(path.dirname(__file__))
    with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
        return f.read()


setup(name='datefns',
      version='0.0.1a8',
      description='A module providing some useful date functions',
      url='https://github.com/ktr/datefns',
      author='Kevin Ryan',
      author_email='ktr@26ocb.com',
      license='MIT',
      long_description=get_long_desc(),
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'Topic :: Software Development :: Build Tools',
          'Topic :: Office/Business',
          'Topic :: Software Development :: Libraries',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
      ],
      keywords='dates',
      packages=find_packages(exclude=['contrib', 'docs', 'tests']),  # Required
      project_urls={
          # 'Bug Reports': 'https://github.com/pypa/sampleproject/issues',
          # 'Funding': 'https://donate.pypi.org',
          # 'Say Thanks!': 'http://saythanks.io/to/example',
          # 'Source': 'https://github.com/pypa/sampleproject/',
      },
      zip_safe=False)
