"""The setup script."""

from setuptools import setup

with open('README.md', encoding='utf-8') as readme_file:
    readme = readme_file.read()

setup(
    name='heaserver-trash-aws-s3',
    version='1.0.0b9',
    description="deleted file management",
    long_description=readme,
    long_description_content_type='text/markdown',
    url='https://risr.hci.utah.edu',
    author="Research Informatics Shared Resource, Huntsman Cancer Institute, Salt Lake City, UT",
    author_email='Andrew.Post@hci.utah.edu',
      python_requires='>=3.10',
      package_dir={'': 'src'},
      packages=['heaserver.trashawss3'],
      package_data={'heaserver.trashawss3': ['wstl/*.json']},
      install_requires=[
          'heaserver>=1.0.0b10, <1.0.0b11',
          'aiostream~=0.5.1'
      ],
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Environment :: Console',
          'Intended Audience :: Developers',
          'Natural Language :: English',
          'License :: OSI Approved :: Apache Software License',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.10',
          'Programming Language :: Python :: Implementation :: CPython',
          'Topic :: Software Development',
          'Topic :: Scientific/Engineering',
          'Topic :: Scientific/Engineering :: Bio-Informatics',
          'Topic :: Scientific/Engineering :: Information Analysis',
          'Topic :: Scientific/Engineering :: Medical Science Apps.'
      ],
    entry_points={
        'console_scripts': [
            'heaserver-trash-aws-s3=heaserver.trashawss3.service:main',
        ],
    },
    keywords=['heaserver-trash-aws-s3', 'microservice', 'healthcare', 'cancer', 'research', 'informatics'],
)
