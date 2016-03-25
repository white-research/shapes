from setuptools import setup

setup(name='shapes',
    version='0.1.2.2',
    description='Tools for analyzing geometric morphometic shape',
    url='http://github.com/DominicWhite/shapes',
    author='Dominic White',
    author_email='dewhite4@gmail.com',
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
