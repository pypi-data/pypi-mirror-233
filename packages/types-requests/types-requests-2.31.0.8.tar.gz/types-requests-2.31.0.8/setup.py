from setuptools import setup

name = "types-requests"
description = "Typing stubs for requests"
long_description = '''
## Typing stubs for requests

This is a PEP 561 type stub package for the `requests` package. It
can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
PyCharm, etc. to check code that uses
`requests`. The source for this package can be found at
https://github.com/python/typeshed/tree/main/stubs/requests. All fixes for
types and metadata should be contributed there.

Note: `types-requests` has required `urllib3>=2` since v2.31.0.7. If you need to install `types-requests` into an environment that must also have `urllib3<2` installed into it, you will have to use `types-requests<2.31.0.7`.

See https://github.com/python/typeshed/blob/main/README.md for more details.
This package was generated from typeshed commit `011f24794d334ecbd6bda104a8e57399bd6bcad8` and was tested
with mypy 1.5.1, pyright 1.1.328, and
pytype 2023.8.31.
'''.lstrip()

setup(name=name,
      version="2.31.0.8",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/requests.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=['urllib3>=2'],
      packages=['requests-stubs'],
      package_data={'requests-stubs': ['__init__.pyi', '__version__.pyi', 'adapters.pyi', 'api.pyi', 'auth.pyi', 'certs.pyi', 'compat.pyi', 'cookies.pyi', 'exceptions.pyi', 'help.pyi', 'hooks.pyi', 'models.pyi', 'packages.pyi', 'sessions.pyi', 'status_codes.pyi', 'structures.pyi', 'utils.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      python_requires=">=3.7",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
