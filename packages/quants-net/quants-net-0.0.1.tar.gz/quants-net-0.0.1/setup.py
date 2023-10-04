from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="quants-net",
    version="0.0.1",
    description="Quants Net Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Quants Net",
    author_email="quants-net-py@quants.net",
    url="https://github.com/quants-net/quants-net-py",
    project_urls={
        "Bug Tracker": "https://github.com/quants-net/quants-net-py/issues",
    },
    packages=["quantsnet"],
    #test_suite="tests",
    install_requires=["numpy", "scipy"],
)
