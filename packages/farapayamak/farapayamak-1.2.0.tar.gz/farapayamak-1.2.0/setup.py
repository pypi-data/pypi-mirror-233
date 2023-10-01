import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="farapayamak",
    version="1.2.0",
    author="Amirhossein Mehrvarzi",
    author_email="farapayamakdev@gmail.com",
    description="Farapayamak REST and SOAP Webservice Wrapper (SDK)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/farapayamak/python",
    project_urls={
        "Bug Tracker": "https://github.com/farapayamak/python/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)