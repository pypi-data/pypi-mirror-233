import setuptools

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name='actiontest',
    author='Drew Shelton',
    author_email='dshelts9306@gmail.com',
    description='actiontest PyPI (Python Package Index) Package',
    keywords='actiontest, pypi, package',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/a-shelton-test-org/actiontest',
    project_urls={
        'Documentation': 'https://github.com/a-shelton-test-org/actiontest',
        'Bug Reports':
        'https://github.com/a-shelton-test-org/actiontest/issues',
        'Source Code': 'https://github.com/a-shelton-test-org/actiontest',
        # 'Funding': '',
        # 'Say Thanks!': '',
    },
    package_dir={'': 'src'},
    packages=setuptools.find_packages(where='src'),
    classifiers=[
        # see https://pypi.org/classifiers/
        'Development Status :: 5 - Production/Stable',

        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'Programming Language :: Python :: 3.11',        
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.11',
    # install_requires=['Pillow'],
    extras_require={
        'dev': ['check-manifest'],
        # 'test': ['coverage'],
    },
)
