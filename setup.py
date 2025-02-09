from setuptools import find_packages, setup
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.1.1'
DESCRIPTION = 'Accelerometer based on chip mpu 6050...'
LONG_DESCRIPTION = 'Accelerometer based on chip mpu 6050.'

# Setting up
setup(
    name="ZemaxFilesBuilderUtils",
    version=VERSION,
    author="YuryStrelkov (Yury Strelkov)",
    author_email="<ghost_strelkov@mail.ru>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['numpy', 'matplotlib', 'pyqt5', 'python-docx', 'pillow', 'numba', 'python-docx'],
    keywords=['Zemax', 'Raytracing', 'Zemax file'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ])
