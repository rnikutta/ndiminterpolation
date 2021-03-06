from setuptools import setup, find_packages

setup(
    name = 'ndiminterpolation',
    version = '1.0.1',
    url = 'https://github.com/rnikutta/ndiminterpolation.git',
    author = 'Robert Nikutta',
    author_email = 'robert.nikutta@gmail.com',
    description = 'Description of my package',
    packages = find_packages(),    
    install_requires = ['numpy', 'scipy', 'matplotlib'],
    zip_safe = False,
)
