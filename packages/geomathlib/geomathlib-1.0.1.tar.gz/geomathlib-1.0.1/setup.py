from setuptools import setup, find_packages

with open('README.md', 'r') as file:
    long_description = file.read()
setup(
    name="geomathlib",
    version="1.0.1",
    description="A library for geometric calculations",
    long_description=long_description,
    long_description_content_type='text/markdown',
    author="Alexandr Medvedev",
    author_email="alex.mmdvdvv@gmail.com",
    packages=find_packages(),
    install_requires=[],
)
