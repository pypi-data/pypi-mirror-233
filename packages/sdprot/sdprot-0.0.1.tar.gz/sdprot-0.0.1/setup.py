from setuptools import setup, find_packages
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='sdprot',
  version='0.0.1',
  description='A Python package that generates and checks passwords, enhancing security and usability in applications',
  long_description=long_description,
  long_description_content_type="text/markdown",
  url='',  
  author='Supratim Das',
  author_email='supratim0707@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords=['sdprot'],
  include_package_data=True, 
  packages=['sdprot'],
  install_requires=['numpy', 'bcrypt', 'datetime'] 
)
