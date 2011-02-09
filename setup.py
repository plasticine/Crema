from setuptools import setup, find_packages

setup(
    name='crema',
    version=__import__('crema').__version__,
    description='A middleware class to help out with coffeescript.',
    author='Justin Morris',
    author_email='justin@pixelbloom.com',
    url='http://pixelbloom.github.com/crema/',
    download_url='http://github.com/pixelbloom/crema/downloads',
    license='BSD',
    packages=find_packages(exclude=['ez_setup']),
    include_package_data=True,
)