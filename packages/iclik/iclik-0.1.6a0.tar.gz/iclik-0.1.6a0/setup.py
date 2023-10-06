from setuptools import setup

setup(
    name='iclik',
    version='0.1.6-alpha',
    packages=['iclik'],
    description="Information criteria for composite likelihood models",
    long_description=open('README.rst').read(),
    long_description_content_type='text/x-rst',
    install_requires=[
        "numdifftools",
        "numpy",
        "scipy"
    ]
)
