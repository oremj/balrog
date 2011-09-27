from setuptools import setup, find_packages
setup(
    name = "AUS",
    version = "0.1",
    packages = find_packages(),
    scripts = ['AUS-server.py', 'client.wsgi'],
    install_requires = ['sqlalchemy==0.7.1', 'flask==0.7.2', 'simplejson']
)
