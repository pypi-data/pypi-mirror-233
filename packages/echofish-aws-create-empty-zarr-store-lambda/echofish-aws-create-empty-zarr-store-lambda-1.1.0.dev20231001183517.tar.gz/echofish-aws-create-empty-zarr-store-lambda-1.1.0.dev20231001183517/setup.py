import setuptools

with open("README.md", "r") as fh:
  long_description = fh.read()

with open('requirements.txt') as f:
  requirements = f.read().splitlines()

setuptools.setup(
  name="echofish-aws-create-empty-zarr-store-lambda",
  version="1.1.0.dev20231001183517",
  description="",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://github.com/ci-cmg/echofish-aws-create-empty-zarr-store-lambda",
  package_dir={'': 'src'},
  packages=setuptools.find_packages('src'),
  classifiers=[
    "Programming Language :: Python :: 3.9",
    "License :: OSI Approved :: MIT License",
  ],
  python_requires='>=3.9',
  install_requires=[req for req in requirements if req[:2] != "# "]
)
