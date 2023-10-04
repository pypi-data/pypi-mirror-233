from setuptools import setup, find_packages

setup(
    name="ohnlptk-xlang-python",
    version="2.0.2",
    description="Python support for OHNLP Toolkit Components",
    author="Andrew Wen",
    author_email="contact@ohnlp.org",
    packages=find_packages(),
    python_requires='>3.7',
    install_requires=[
        'py4j==0.10.9.7'
    ]
)
