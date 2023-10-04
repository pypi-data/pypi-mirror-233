from setuptools import setup, find_packages

setup(
    name="python-advanced-typing",
    version="0.8",
    packages=find_packages(),
    install_requires=[],
    author="Yidi Sprei",
    author_email="yididev@gmail.com",
    description="An intuitive Python utility to ensure type accuracy in your code. With capabilities to validate single or multiple variables, it streamlines type verification, boosting code reliability and readability.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/YidiSprei/PythonAdvancedTyping",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
