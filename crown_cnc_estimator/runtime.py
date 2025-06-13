"""Simple runtime calculations."""


def calculate_runtime(feed_rate: float, path_length: float) -> float:
    """Return runtime given feed_rate (units/min) and path_length (units)."""
    if feed_rate <= 0:
        raise ValueError("feed_rate must be greater than zero")
    return path_length / feed_rate


def calculate_material_removal_rate(
    feed_rate: float, width_of_cut: float, depth_of_cut: float
) -> float:
    """Return material removal rate in volume per minute.

    The calculation multiplies the feed rate by the radial (width) and axial
    (depth) engagement of the tool::

        MRR = feed_rate * width_of_cut * depth_of_cut

    ``feed_rate`` must be greater than zero while ``width_of_cut`` and
    ``depth_of_cut`` must be non-negative.
    """

    if feed_rate <= 0:
        raise ValueError("feed_rate must be greater than zero")
    if width_of_cut < 0 or depth_of_cut < 0:
        raise ValueError("cut dimensions must be non-negative")
    return feed_rate * width_of_cut * depth_of_cut
