from pyhdf.SD import SD, SDC
import numpy as np

FILE_PATH = "data/MOD06_L2.A2021196.0000.061.2021269014955.hdf"

def load_cloud_thickness():
    hdf = SD(FILE_PATH, SDC.READ)

    # MODIS Optical Thickness (1km)
    ds = hdf.select("Cloud_Optical_Thickness")
    raw = ds[:].astype(np.float32)

    attrs = ds.attributes()

    fill = attrs["_FillValue"]
    valid_min, valid_max = attrs["valid_range"]
    scale = attrs["scale_factor"]
    offset = attrs["add_offset"]

    # mask invalid
    raw[raw == fill] = np.nan
    raw[(raw < valid_min) | (raw > valid_max)] = np.nan

    # apply scaling
    cot = raw * scale + offset

    print("Cloud Optical Thickness loaded ✅")
    print("COT shape:", cot.shape)
    print(
        "COT min/max:",
        np.nanmin(cot),
        np.nanmax(cot)
    )

    return cot


# direct test
if __name__ == "__main__":
    load_cloud_thickness()
