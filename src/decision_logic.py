def classify_seedability(ctt, depth, dbz):
    """
    Classifies cloud seedability based on objective criteria

    Parameters:
    ctt   : Cloud Top Temperature (°C)
    depth : Cloud depth / thickness proxy (km or normalized)
    dbz   : Radar reflectivity proxy (dBZ or equivalent)

    Returns:
    green, amber, gray : boolean masks
    """

    # -------------------------
    # GREEN: High seedability
    # Strong cloud, good SLW, ideal temp
    # -------------------------
    green = (
        (ctt < -10) &
        (depth > 2) &
        (dbz >= 20) & (dbz <= 35)
    )

    # -------------------------
    # AMBER: Marginal / uncertain
    # Borderline in ANY one parameter
    # -------------------------
    amber = (
        (~green) & (
            ((ctt >= -10) & (ctt <= -5)) |
            ((depth >= 1) & (depth <= 2)) |
            ((dbz >= 15) & (dbz < 20))
        )
    )

    # -------------------------
    # GRAY: Not seedable
    # -------------------------
    gray = ~(green | amber)

    return green, amber, gray
