import os

from setuptools import setup


def get_version():
    print(os.getcwd())
    with open("version.txt", "r", encoding="utf-8") as file:
        return file.read().split("\n")[0].strip()


def read_requirements():
    with open("requirements.txt", "rt", encoding="utf-8") as fin:
        raw_requirements = fin.readlines()
    return list(map(lambda x: x[:-1], raw_requirements))


def readme():
    with open("README.md", "rt") as fin:
        readme_text = fin.read()
    return readme_text


setup(
    name="pyreq-merger",
    version=get_version(),
    description="Merge 2 requirement files into a single file, using the specified method.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/mhristodor/pyreq-merger",
    author="mhristodor",
    author_email="minumh99@gmail.com",
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.11",
    ],
    keywords="requirements merge tool",
    project_urls={
        "Documentation": "https://github.com/mhristodor/pyreq-merger/blob/main/README.md",
        "Source": "https://github.com/mhristodor/pyreq-merger",
        "Tracker": "https://github.com/mhristodor/pyreq-merger/issues",
        "Author": "https://www.linkedin.com/in/mihail-hristodor-1174b2177/",
        "Funding": "https://www.buymeacoffee.com/m.hristodor",
    },
    install_requires=read_requirements(),
    python_requires=">=3.11",
    entry_points="""
    [console_scripts]
    pyreq = pyreqmerger.main:main
    """,
)
