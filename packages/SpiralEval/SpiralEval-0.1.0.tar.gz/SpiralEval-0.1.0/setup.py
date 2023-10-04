from setuptools import setup, find_packages
import re

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("spiraleval/__init__.py") as f:
    init_text = f.read()
    version = re.search(r"__version__\s*=\s*[\'\"](.+?)[\'\"]", init_text).group(1)

setup(
    name="SpiralEval",
    version=version,
    url="https://github.com/Spiral-AI/SpiralEval",
    author="Kosei Uemura",
    author_email='koseiuemura1227@gmail.com',
    description="Evaluation for characteristics",
    packages=find_packages(),
    install_requires=['openai', 'pandas'],
    python_requires='>=3.8, <4',
    keywords="openai, api, evaluation, characteristics, gpt",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)
