from setuptools import setup

setup (
    name="tornadoAPI",
    package=["tornadoAPI"],
    include_package_data=True,
    install_requires=[
        "tornado",
        "multiprocessing",
        "gevent",
        "logging",
    ]
)
