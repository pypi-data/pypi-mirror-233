from setuptools import setup, find_packages

setup(
    name='keaml',
    version='0.1.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'joblib==1.3.2'
    ],
    author='Gabriel Obaldia',
    author_email='support@keaml.com',
    description='KeaML Python SDK',
    long_description_content_type="text/markdown",
    long_description=open('README.md').read(),
)
