"""Rpc Client Errors"""

class RpcFailure(Exception):
    """Raises whenever the server replies with an rpc error message."""
    