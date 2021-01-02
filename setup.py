from setuptools import setup, find_packages

with open("README.md","r") as rf:
	readme = rf.read()

requirements = ["requests>=2"]

setup(
	name = "amazoncapApi",
	version = "0.0.1",
	author = "Harshawardhan Natu",
	author_email = "harsh.natu.3@gmail.com",
	description = "A package to solve captcha when collecting data from Amazon.",
	long_description = readme,
	long_description_content_type = "text/markdown",
	url = "https://github.com/HRN-Projects/amazon-captcha-solver",
	packages=find_packages(),
	install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
)