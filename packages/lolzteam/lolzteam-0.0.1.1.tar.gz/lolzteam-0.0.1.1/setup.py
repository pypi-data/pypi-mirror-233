import setuptools

# with open("README.md", "r") as fh:
#     long_description = fh.read()
long_description = "Placeholder for lib transfer"

requirements = []

setuptools.setup(
    name="lolzteam",
    version="0.0.1.1",
    author="AS7RID",
    author_email="as7ridwork@gmail.com",
    description="Placeholder for lib transfer",
    long_description=long_description,
    long_description_content_type="text/markdown",
    # url="https://github.com/AS7RIDENIED/Lolzteam_Python_Api",
    packages=setuptools.find_packages(),
    install_requires=requirements,
    classifiers=["Programming Language :: Python :: 3.11"],
    python_requires='>=3.9'
)
