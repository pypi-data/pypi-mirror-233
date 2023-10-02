from setuptools import setup, find_packages

setup(
    name='logging-library',
    version='0.2.0',
    packages=find_packages(),
    install_requires=[],
    tests_require=[],
    entry_points={},
    url='https://gitlab.com/adv_python_maglnuse/assignment3',
    license='MIT',
    author='maglnuse',
    author_email='n_maulen@kbtu.kz',
    description='A custom logging library',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)