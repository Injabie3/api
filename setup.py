from setuptools import find_packages, setup

setup(
    name="injabie3-api",
    version="0.0.1",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "Flask==1.1.4",
        "flask-restx==0.5.1",
    ],
)
