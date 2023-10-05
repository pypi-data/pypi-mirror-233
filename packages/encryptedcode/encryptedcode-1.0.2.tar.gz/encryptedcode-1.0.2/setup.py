from setuptools import find_packages, setup

readme = open("./README.md","r")

setup(
    name='encryptedcode',
    python_version='3.11.0',
    version='1.0.2',
    description='This library can be used to encrypt and decrypt passwords using a new L0123 algorithm.',
    long_description=readme.read(),
    long_description_content_type='text/markdown',
    author='Leandro Gonzalez Espinosa',
    author_email='lworkgonzalez01@gmail.com',
    packages=['encryptedcode'],
    keywords=['encrypt','encode'],
    url='https://github.com/leoGlez01/password_encode.git',
    license='MIT',
    include_package_data=True
)