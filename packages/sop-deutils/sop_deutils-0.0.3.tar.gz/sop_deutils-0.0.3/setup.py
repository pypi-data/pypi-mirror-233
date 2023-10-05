from setuptools import setup, find_packages

setup(
    name="sop_deutils",
    version="0.0.3",
    author="liuliukiki",
    author_email="longnc@yes4all.com",
    description="A utils package for Yes4All SOP",
    long_description="README.md",
    long_description_content_type="text/markdown",
    python_requires=">=3.7",
    install_requires=[
        "openpyxl>=3.1.2",
        "pytz>=2023.3",
        "pandas>=2.1.1",
        "python-telegram-bot>=20.6",
        "SQLAlchemy>=2.0.21",
        "lxml>=4.9.3",
        "gspread>=5.11.3",
        "psycopg2-binary>=2.9.9",
        "minio>=7.1.17",
        "pyarrow>=13.0.0",
        "requests>=2.31.0",
        "aiofiles>=23.2.1",
        "fastparquet>=2023.8.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    url="https://github.com/dribblewithclong",
    project_urls={
        "Author Github": "https://github.com/dribblewithclong",
    },
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
)
