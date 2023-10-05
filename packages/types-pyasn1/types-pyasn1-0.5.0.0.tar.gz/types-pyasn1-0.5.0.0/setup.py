from setuptools import setup

name = "types-pyasn1"
description = "Typing stubs for pyasn1"
long_description = '''
## Typing stubs for pyasn1

This is a PEP 561 type stub package for the `pyasn1` package. It
can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
PyCharm, etc. to check code that uses
`pyasn1`. The source for this package can be found at
https://github.com/python/typeshed/tree/main/stubs/pyasn1. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/main/README.md for more details.
This package was generated from typeshed commit `25eb99cbec6d791558bce4b5b224e307ce755029` and was tested
with mypy 1.5.1, pyright 1.1.328, and
pytype 2023.8.31.
'''.lstrip()

setup(name=name,
      version="0.5.0.0",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/pyasn1.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=[],
      packages=['pyasn1-stubs'],
      package_data={'pyasn1-stubs': ['__init__.pyi', 'codec/__init__.pyi', 'codec/ber/__init__.pyi', 'codec/ber/decoder.pyi', 'codec/ber/encoder.pyi', 'codec/ber/eoo.pyi', 'codec/cer/__init__.pyi', 'codec/cer/decoder.pyi', 'codec/cer/encoder.pyi', 'codec/der/__init__.pyi', 'codec/der/decoder.pyi', 'codec/der/encoder.pyi', 'codec/native/__init__.pyi', 'codec/native/decoder.pyi', 'codec/native/encoder.pyi', 'codec/streaming.pyi', 'compat/__init__.pyi', 'compat/integer.pyi', 'compat/octets.pyi', 'debug.pyi', 'error.pyi', 'type/__init__.pyi', 'type/base.pyi', 'type/char.pyi', 'type/constraint.pyi', 'type/error.pyi', 'type/namedtype.pyi', 'type/namedval.pyi', 'type/opentype.pyi', 'type/tag.pyi', 'type/tagmap.pyi', 'type/univ.pyi', 'type/useful.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      python_requires=">=3.7",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
