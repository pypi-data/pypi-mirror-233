from setuptools import setup, find_packages
from pathlib import Path

here = Path(__file__).parent

setup(
    name="servicenow-utils",
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    url="https://github.com/reese-001/servicenow-utils/blob/main/setup.py",
    long_description=(here / "README.md").read_text(encoding="utf-8"),
    long_description_content_type="text/markdown",
    include_package_data=True,
    version="0.20",
    packages=find_packages(),
    install_requires=[
        'requests',
        'pandas'
    ],
    description="A utility module for retrieving incidents from ServiceNow",
    keywords="servicenow incidents utility",
    license="MIT",
    # url="https://github.com/yourusername/servicenow-utils",  # If you host it on GitHub or another platform
)
