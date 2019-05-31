import setuptools

requires = [
    # asyncio was added to the stdlib in Python v3.4
    'asyncio; python_version < "3.4"',
    'aiohttp',
    'aiodns',
    'pandas',
    'tqdm',
    'requests',
]

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cmc",
    version="2.0.3.1",
    author="Alejandro Escontrela <alejandroescontrela@gmail.com>,Felipe Faria <felipefaria@me.com>",
    author_email="alejandroescontrela@gmail.com",
    description="Get the price history for CoinMarketCap-listed currencies",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Alescontrela/coinmarketcap-history",
    packages=setuptools.find_packages(),
    install_requires=requires,
    entry_points={
        "console_scripts": [
            "coinmarketcap=cmc.coinmarketcap:main",
        ],
    },
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
