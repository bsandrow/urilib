"""\
urilib.api

Where all of the API peices reside.
"""

from urilib.uri import URI

def uri(*args, **kwargs):
    return URI(*args, **kwargs)
