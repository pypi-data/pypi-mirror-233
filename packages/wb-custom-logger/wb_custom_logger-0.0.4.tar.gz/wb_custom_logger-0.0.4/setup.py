from setuptools import setup, find_packages

setup(
    name='wb_custom_logger',
    version='0.0.4',
    description='',
    url='https://wavebridge.com',
    author='Tom Choi',
    author_email='tom.choi@wavebridge.com',
    license='(c) WaveBridge',
    packages=find_packages(exclude=["test"]),
    classifiers=[
        "Programming Language :: Python :: 3.10",
    ],
    install_requires=[
    ],
    zip_safe=False
)
