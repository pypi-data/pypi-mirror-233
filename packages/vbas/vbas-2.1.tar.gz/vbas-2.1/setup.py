import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="vbas", # Replace with your own username
    version="2.1",
    author="DoubleEight",
    author_email="fanta09tv@gmail.com",
    description="ValorantBot Api System",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/teamdoubleeight/vbas",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    requires=["requests","urllib3","aiohttp"]
)