from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

v='0.1.3'

setup(name='shapes',
    version = v,
    description='Tools for analyzing geometric morphometic shape',
    url='http://github.com/DominicWhite/shapes',
    author='Dominic White',
    author_email='dewhite4@gmail.com',
    long_description = long_description,
    long_description_content_type = "text/markdown",
    license='MIT',
    packages=['shapes'],
    install_requires=[
        'numpy',
        'matplotlib'
    ],
    zip_safe=False,
    test_suite='nose.collector',
    tests_require=['nose'],
    )
