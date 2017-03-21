class UnsupportedVersion(Exception):
    """Indicates that the user is trying to use an UnsupportedVersion
    version of the API.
    """
    pass


class EndpointNotFound(Exception):
    """Could not find Service or Region in Service Catalog."""
    pass


class APIInternalError(Exception):
    """API build error"""
    pass
