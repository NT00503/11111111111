from setuptools import setup, find_packages

setup(
    name="data_viz_tool",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "matplotlib",
        "requests",
        "openai",
    ],
    entry_points={
        "console_scripts": [
            "data_viz_tool=data_viz_project.main:data_viz_tool"
        ]
    },
    author="Your Name",
    description="A package for fetching and visualizing open data using OpenAI.",
    url="https://github.com/yourusername/data_viz_tool",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
