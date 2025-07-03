from setuptools import setup, find_packages

def get_requirements():
    with open('requirment.txt', 'r') as f:
        libs = f.read().splitlines()
        libs.pop()
    return libs


setup(
    name='mlproj2',
    version='0.1.0',
    author = "sarfraz",
    packages=find_packages(),
    install_requires=get_requirements(),
    description='A machine learning project template',
)