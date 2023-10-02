from setuptools import setup, find_packages

setup(
    name="ip2vulns",
    version="0.1",
    packages=find_packages(),
    author="Your Name",
    description="A description of your package",
    install_requires=[],
    entry_points = {
        'console_scripts': [
            'ip2vulns = ip2vulns.ip2vulns:main'
        ]
    }
)
