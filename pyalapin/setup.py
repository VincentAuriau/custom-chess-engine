from setuptools import setup, find_packages

VERSION = "0.0.1"
DESCRIPTION = "pyalapin is a customized chess engine, specifically to work with AIs."
LONG_DESCRIPTION = """Is it the best, most efficient and state of the art chess engine ? I'm pretty sure not.

However, driven by passion and madness, I have developed my own chess game in Python. For your pretty eyes and your devilish smile, I share it with you. But only with you.

Special thanks and dedication to LeMerluche, crushing its opponents on chess.com with alapin openings ❤️"""

# Setting up
setup(
    name="pyalapin",
    version=VERSION,
    author="Vincent Auriau",
    author_email="",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=["numpy"],
    keywords=["python", "first package"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Anyone",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: Linux :: Linux",
    ],
)
