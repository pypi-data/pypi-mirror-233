from setuptools import setup, find_packages

VERSION = '0.1'
DESCRIPTION = 'A Python library for encryption and decryption.'

# Setting up
setup(
    name="OsYEncrypt",
    version=VERSION,
    author="Osama Mohammed",
    author_email="osama.paaall@gmail.com",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'encryption', 'decryption', 'security'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
