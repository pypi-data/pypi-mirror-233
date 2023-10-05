from setuptools import setup, find_packages


def get_readme():
    with open("README.md", "r") as file:
        return file.read()


setup(
  name='book-system-SDK',
  version='0.1.6',
  author='Artem Sydorenko',
  author_email='kradworkmail@gmail.com',
  description='SDK for interaction with the book-system API',
  long_description=get_readme(),
  long_description_content_type='text/markdown',
  packages=find_packages(),
  classifiers=[
    'Programming Language :: Python :: 3.11'
  ],
  python_requires='>=3.11'
)
