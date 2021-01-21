import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="SmtApi", # Replace with your own username
    version="v0.1.5a1",
    author="Joshua Edwards",
    author_email="joshua.edwards.navy@gmail.com",
    description="An API for SmartMeterTexas",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Inaruslynx/SmtApi",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)