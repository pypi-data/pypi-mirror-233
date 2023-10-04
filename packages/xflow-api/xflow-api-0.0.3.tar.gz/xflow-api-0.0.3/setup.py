from setuptools import setup, find_packages

setup(
    name='xflow-api',
    version='0.0.3',
    description='python package for xflow',
    author='kyon',
    author_email='originky2@gmail.com',
    install_requires=['ray', 'dill', 'ipython', 'pydantic',],
    packages=find_packages(exclude=[]),
    python_requires='>=3.10',
    package_data={},
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python :: 3.11',
    ],
)