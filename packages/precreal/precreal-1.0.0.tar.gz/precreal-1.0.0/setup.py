from setuptools import setup
setup(
    name="precreal",
    version="1.0.0",
    description="A package providing a fraction-based Real class that allows you to do exact real arithmetic, along with some algorithms",
    author="None1",
    packages=["precreal"],
    keywords=["arithmetic", "calculating", "real number"],
    python_requires=">=3",
    url="https://github.com/none-None1/precreal",
    long_description=open("README.md", "r").read(),
    long_description_content_type="text/markdown",
    entrypoints={"console_scripts": ["precreal_test=precreal.test:_test"]},
)
