import pathlib as p

import setuptools

SOURCE_URL = "https://example.com/" # Placeholder

DEPENDENCIES = [
  "colored",
]

setuptools.setup(
  name="tcrutils",
  version="0.0.1",
  description="Useful stuff for tcr projects",
  long_description=p.Path('README.md').read_text(),
  long_description_content_type='text/markdown',
  url=SOURCE_URL,
  author="TheCreatorrrr",
  license="The Unlicense",
  project_urls={
    "Source": SOURCE_URL,
  },
  classifiers=[
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Topic :: Utilities",
  ],
  python_requires=">=3.10,<3.12",
  install_requires=DEPENDENCIES,
  packages=setuptools.find_packages(),
  include_package_data=True,
) 