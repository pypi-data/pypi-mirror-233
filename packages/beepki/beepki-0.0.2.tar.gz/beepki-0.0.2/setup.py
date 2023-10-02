from setuptools import setup, find_packages

setup(
    name='beepki',
    version='0.0.2',
    license='Apache 2.0',
    author='Zeio Nara',
    author_email='zeionara@gmail.com',
    packages=find_packages(),
    description='A simple module for making signal when exiting from a block',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url='https://github.com/zeionara/beep',
    project_urls={
        'Documentation': 'https://github.com/zeionara/beep#readme',
        'Bug Reports': 'https://github.com/zeionara/beep/issues',
        'Source Code': 'https://github.com/zeionara/beep'
    },
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3.11"
    ],
    install_requires = ['numpy', 'pygame']
)
