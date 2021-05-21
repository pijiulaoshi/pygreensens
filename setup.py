import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pygreensens",
    version="0.3.6",
    author="PijiuLaoshi",
    author_email="pijiulaoshi@gmail.com",
    description="Python package for GreenSens Plant Sensor Api",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pijiulaoshi/pygreensens",
    project_urls={
        "Bug Tracker": "https://github.com/pijiulaoshi/pygreensens/issues",
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
