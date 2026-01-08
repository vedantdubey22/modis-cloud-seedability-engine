from pyhdf.SD import SD, SDC
import numpy as np

FILE_PATH = "data/MOD06_L2.A2021196.0000.061.2021269014955.hdf"


def load_ctt():
    hdf = SD(FILE_PATH, SDC.READ)

    ds = hdf.select("Cloud_Top_Temperature")
    raw = ds[:].astype(np.float32)

    attrs = ds.attributes()

    fill = attrs["_FillValue"]
    valid_min, valid_max = attrs["valid_range"]
    scale = attrs["scale_factor"]   # usually 0.01

    # mask invalid
    raw[raw == fill] = np.nan
    raw[(raw < valid_min) | (raw > valid_max)] = np.nan

    # apply scaling → Kelvin
    ctt_kelvin = raw * scale

    # Kelvin → Celsius
    ctt_celsius = ctt_kelvin - 273.15

    print("CTT loaded correctly ✅")
    print("CTT shape:", ctt_celsius.shape)
    print(
        "CTT min/max (°C):",
        np.nanmin(ctt_celsius),
        np.nanmax(ctt_celsius),
    )

    return ctt_celsius


if __name__ == "__main__":
    load_ctt()
