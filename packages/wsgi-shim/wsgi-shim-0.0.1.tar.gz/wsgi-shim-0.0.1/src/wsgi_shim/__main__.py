"""The wsgi_shim package CLI entry point"""
from .wsgi_shim import cli  # pragma no cover


# Enable `python -m wsgi_shim ...`
if __name__ == "__main__":  # pragma no cover
    raise SystemExit(cli())
