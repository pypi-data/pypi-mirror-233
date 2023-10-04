from setuptools import setup

name = "types-regex"
description = "Typing stubs for regex"
long_description = '''
## Typing stubs for regex

This is a PEP 561 type stub package for the `regex` package. It
can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
PyCharm, etc. to check code that uses
`regex`. The source for this package can be found at
https://github.com/python/typeshed/tree/main/stubs/regex. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/main/README.md for more details.
This package was generated from typeshed commit `d60e66712a55df1fda94daf511c9c764d112e1ff` and was tested
with mypy 1.5.1, pyright 1.1.328, and
pytype 2023.8.31.
'''.lstrip()

setup(name=name,
      version="2023.10.3.0",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/regex.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=[],
      packages=['regex-stubs'],
      package_data={'regex-stubs': ['__init__.pyi', '_regex.pyi', '_regex_core.pyi', 'regex.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      python_requires=">=3.7",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
