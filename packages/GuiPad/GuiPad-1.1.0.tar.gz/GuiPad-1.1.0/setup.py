from setuptools import setup, find_packages
import codecs
import os

with codecs.open(os.path.join(os.path.abspath(os.path.dirname(__file__)), "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '1.1.0'
DESCRIPTION = 'Use your gamepad as a mouse with pygame and PyAutoGUI.'
LONG_DESCRIPTION = 'A simple module to use your gamepad as a mouse with pygame and PyAutoGUI.'

# Setting up
setup(
    name="GuiPad",
    version=VERSION,
    url ="https://github.com/JackLawrenceCRISPR/GuiPad",
    author="Jack Lawrence",
    author_email="<JackLawrenceCRISPR@gmail.com>",
    license="MIT",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=["pygame>=2.0.0","pyautogui>0.9.0"],
    python_requires=">=3.0",
    keywords=['python', 'pygame', 'pyautogui', 'gamepad'],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
	"Intended Audience :: End Users/Desktop",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
	"License :: OSI Approved :: MIT License",
	"Natural Language :: English",
    ]
)