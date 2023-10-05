from setuptools import setup

setup(
        py_modules=['douglog'],
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


