from setuptools import find_packages, setup

setup(
    name="injabie3-api",
    version="0.0.1",
    packages=["injabie3api", "injabie3api.system"],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "Werkzeug==1.0.1",
        "markupsafe==2.0.1",
        "Flask==1.1.4",
        "flask-restx==0.5.1",
    ],
)
