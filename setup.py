import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="licensevalidator",
    version="1.2.3",
    description="A validator for dependency licenses",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/eclipse-velocitas/license-check",
    packages=["licensevalidator", "licensevalidator.lib"],
    package_data={"licensevalidator": ["py.typed"]},
    include_package_data=True,
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache License 2.0",
        "Operating System :: OS Independent",
    ],
)
