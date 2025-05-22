import shortuuid

def generate_short_code(length=8):
    """
    Generates a unique, URL-safe short code.
    """
    # shortuuid provides a concise, URL-safe ID using base58 by default
    return shortuuid.uuid()[:length]