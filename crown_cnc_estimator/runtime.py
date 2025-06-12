"""Simple runtime calculations."""


def calculate_runtime(feed_rate: float, path_length: float) -> float:
    """Return runtime given feed_rate (units/min) and path_length (units)."""
    if feed_rate <= 0:
        raise ValueError("feed_rate must be greater than zero")
    return path_length / feed_rate
