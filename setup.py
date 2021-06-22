import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gitmixin",
    version="0.1.0",
    author="Patrick Hastings",
    author_email="phastings@gnubyte.com",
    description="An SQL-Alchemy mixin to give records per row a git version tracked text",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gnubyte/gitmixin",
    project_urls={
        "Bug Tracker": "https://github.com/gnubyte/gitmixin/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "gitmixin"},
    packages=setuptools.find_packages(where="gitmixin"),
    python_requires=">=3.6",
)