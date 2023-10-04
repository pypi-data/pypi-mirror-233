from setuptools import setup, find_packages

# This will make the README.md file shows up in pypi home page
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="labeeb",  # this is what people pip install
    version="0.0.1",
    author="Mohamed Eldesouki",
    author_email="labeeb@eldesouki.com",
    description="A deep learning engine made easy",
    long_description=long_description,
    long_description_content_type="text/markdown",
    py_modules=[  # this is what people import "import user_pb2"
        "__init__"
    ],
    url="https://github.com/disooqi/labeeb",
    project_urls={
        "Bug Tracker": "https://github.com/disooqi/labeeb/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: The Unlicense (Unlicense)",
        "Operating System :: POSIX :: Linux",
    ],
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.11",
    install_requires=['grpcio-tools~=1.58'],
    extras_require=dict(
        dev=['pytest', 'bump2version', 'check-manifest'],
        tests=['pytest', 'bump2version'],
        versioning=['bump2version'],
    )

)
