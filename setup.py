import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cmc",
    version="2.0.2",
    author="Alejandro Escontrela,Felipe Faria",
    author_email="alejandroescontrela@gmail.com, felipefaria@me.com",
    description="Get the price history for CoinMarketCap-listed currencies",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Alescontrela/coinmarketcap-history",
    packages=setuptools.find_packages(),
    scripts=['bin/coinmarketcap'],
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
