from pyhdf.SD import SD, SDC
import numpy as np

FILE_PATH = "data/MOD06_L2.A2021196.0000.061.2021269014955.hdf"


def load_cloud_phase():
    """
    Loads MODIS Cloud Phase (Infrared)

    Returns:
    phase_raw  : raw phase values
    phase_mask : dict of boolean masks
                 (water, ice, mixed, clear)
    """

    hdf = SD(FILE_PATH, SDC.READ)

    ds = hdf.select("Cloud_Phase_Infrared")
    raw = ds[:].astype(np.float32)

    attrs = ds.attributes()

    fill = attrs["_FillValue"]
    valid_min, valid_max = attrs["valid_range"]

    # -------------------------
    # Mask invalid values
    # -------------------------
    raw[raw == fill] = np.nan
    raw[(raw < valid_min) | (raw > valid_max)] = np.nan

    """
    MODIS Cloud Phase (Infrared):
    0 = Clear
    1 = Water
    2 = Ice
    3 = Mixed
    """

    # -------------------------
    # Phase masks (objective use)
    # -------------------------
    water = raw == 1
    ice = raw == 2
    mixed = raw == 3
    clear = raw == 0

    # -------------------------
    # Debug info
    # -------------------------
    print("Cloud Phase loaded ✅")
    print("Shape:", raw.shape)

    phase_stats = {
        "clear": int(np.nansum(clear)),
        "water": int(np.nansum(water)),
        "ice": int(np.nansum(ice)),
        "mixed": int(np.nansum(mixed)),
    }

    print("Phase distribution:", phase_stats)

    phase_mask = {
        "clear": clear,
        "water": water,
        "ice": ice,
        "mixed": mixed,
    }

    return raw, phase_mask


# direct test
if __name__ == "__main__":
    load_cloud_phase()
