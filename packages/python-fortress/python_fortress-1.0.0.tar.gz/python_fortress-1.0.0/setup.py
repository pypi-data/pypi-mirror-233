from setuptools import setup, find_packages

setup(
    name="python_fortress",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        'requests>=2.27,<3',
        'python-dotenv>=0.20,<1'
    ],
    author="Magestree Network S.L.",
    author_email="erick.hernandez@magestree.com",
    description="A Python module to securely interact with passfortress.com API for retrieving and "
                "loading environment variables from a remote .env file.",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/magestree/python_fortress",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
