from setuptools import setup, find_packages

setup(
    name="etl_history",
    version="0.1.1",
    author="Nilesh Sukhwani",
    packages=find_packages(),
    install_requires=[
        "openpyxl",
        "psycopg2-binary",
        "pymysql",
        "sqlalchemy",
        "pandas",
    ],  # List your package dependencies here
)
