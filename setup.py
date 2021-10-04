from setuptools import setup
REQUIRMENTS = ['requests','mypy']

setup(
    name='cartesmapper',
    version='0.1',
    description='Create maps on cartes.io using api',
    url='#',
    author='talha kazi',
    author_email='talhakazi3@gmail.com',
    license='MIT',
    packages=['mapper'],
    install_requires=REQUIRMENTS,
    zip_safe=False
)