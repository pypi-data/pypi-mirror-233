import iplot
from setuptools import setup, find_packages  # type: ignore

long_description = ""
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

requirements = []
with open("requirements.txt", "r") as fh:
    requirements = fh.readlines()

setup(
    name="plotador",
    version=iplot.__version__,
    author="David Alexander",
    author_email="david.tbsilva@gmail.com",
    description="Interface para ilustracao grafica de arquivos de modelos energeticos",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/davidAlexander08/iplot",
    packages=find_packages(),
    package_data={"iplot": ["py.typed"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
)
