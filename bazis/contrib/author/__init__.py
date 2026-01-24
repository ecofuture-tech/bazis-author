try:
    from importlib.metadata import PackageNotFoundError, version
    __version__ = version('bazis-author')
except PackageNotFoundError:
    __version__ = 'dev'
