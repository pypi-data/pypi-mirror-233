from setuptools import setup
from setuptools.command.install import install
import subprocess

# Create a custom install class to run code after installation
class CustomInstall(install):
    def run(self):
        install.run(self)  # Call the original install command
        # Execute your code here
        subprocess.run(["python", "-m", "poc-nvk.my_module"])

setup(
    name="poc-nvk",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="",
    long_description="",
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/poc-nvk",
    packages=["poc-nvk"],
    cmdclass={'install': CustomInstall},  # Use the custom install class
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

