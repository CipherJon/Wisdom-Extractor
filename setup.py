```python
from setuptools import setup, find_packages

setup(
    name="WisdomExtractor",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A tool to extract insights from YouTube videos using AI",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/WisdomExtractor",
    packages=find_packages(),
    install_requires=[
        "streamlit",
        "yt-dlp",
        "openai",
        "python-dotenv",
        "pydantic",
        "SQLAlchemy",
        "pytest",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
