from setuptools import setup, find_packages

setup(
    name="etl_history",
    version="0.1.8",
    author="Nilesh Sukhwani",
    # author_email="your_email@example.com",
    description="A Python package for ETL history management",
    # url="https://github.com/yourusername/etl-history",  # Replace with the URL of your package's repository
    packages=find_packages(),
    install_requires=[
        "openpyxl",
        "pandas",
        "psycopg2-binary",
        "pymysql",
        "sqlalchemy",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Software Development :: Libraries",
        "Topic :: Utilities",
    ],
)
