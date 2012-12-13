"""\
urilib.api

Where all of the API peices reside.
"""

from .uri   import URI
from .query import QueryDict

def uri(*args, **kwargs):
    return URI(*args, **kwargs)

# explicit is better than implicit
__all__ = [ 'URI', 'QueryDict', 'uri' ]
