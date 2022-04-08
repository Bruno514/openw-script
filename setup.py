from setuptools import setup, find_packages

setup(
    name="openw",
    version="0.0.1",
    py_modules=["openw"],
    packages=find_packages(),
    include_package_data=True,
    install_requires=["Click", "requests", "toml"],
    entry_points="""
        [console_scripts]
        openw=openw.main:cli
    """,
)
