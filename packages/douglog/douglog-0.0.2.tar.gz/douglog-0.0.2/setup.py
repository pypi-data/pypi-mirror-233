from setuptools import setup

setup(
        py_modules=['dlog'],
        install_requires=[
            'click',
            'numpy',
            ],
        entry_points={
            'console_scripts': [
                'dlog = src.douglog:dlog',
                ]
            }
        )


