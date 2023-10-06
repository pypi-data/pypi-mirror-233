# Releasing to PyPI

Follow setup instructions from https://docs.google.com/document/d/1fqZWanI8NyfCWcm_1-4CYrvqs43y5AuHNrKdsf1ulkk/edit# to obtain the token.

Put configuration into `~/.pypirc`:

```
[distutils]
index-servers =
    pypi

[pypi]
  username = __token__
  password = <<<token you got>>>
```

Build and push

```bash
python -m build
twine upload dist/*
```
