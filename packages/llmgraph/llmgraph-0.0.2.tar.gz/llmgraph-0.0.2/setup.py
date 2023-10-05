from setuptools import setup, find_packages

version = "0.0.2"

with open("README.md", "r") as f:
    long_description = f.read()

with open("requirements.txt", "r", encoding="utf-8") as f:
    install_requires = [x.strip() for x in f if x.strip()]

setup(
    name="llmgraph",
    version=version,
    description="llmgraph",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dylanhogg",
    author="Dylan Hogg",
    author_email="dylanhogg@gmail.com",
    # https://pypi.org/classifiers/
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    keywords="llm, kg, knowledge graph, chatgpt",
    entry_points={"console_scripts": ["llmgraph=app:typer_app"]},
    package_dir={"": "llmgraph"},
    packages=find_packages("llmgraph", exclude=["tests.*"]),
    python_requires=">=3.8, <4",
    install_requires=install_requires,
)
