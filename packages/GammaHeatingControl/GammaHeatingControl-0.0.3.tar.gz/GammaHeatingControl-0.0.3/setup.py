import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="GammaHeatingControl",
    version="0.0.2",
    author="Patrick Menschel",
    author_email="menschel.p@posteo.de",
    description="A python 3 interface to EBV Gamma Heating Control.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/menschel/GammaHeatingControl",
    packages=setuptools.find_packages(exclude=["tests", ]),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3 :: Only",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Intended Audience :: Developers",
    ],
    python_requires=">=3.7",
    keywords="ebv gamma heating control",
    install_requires=["pyserial", "crccheck"],
    scripts=["bin/gamma_logger.py"]
)
