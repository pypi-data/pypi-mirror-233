from setuptools import setup, find_packages

setup(
        packages=find_packages(),
        install_requires=[
            'click',
            'numpy',
            ],
        entry_points={
            'console_scripts': [
                'dlog = douglog.douglog:dlog',
                ]
            }
        )


