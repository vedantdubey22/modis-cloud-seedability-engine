import numpy as np
import cv2

from cloud_temperature import load_ctt
from cloud_thickness import load_cloud_thickness
from cloud_water_path import load_cloud_water_path
from cloud_phase import load_cloud_phase
from decision_logic import classify_seedability
from color_mapper import create_color_map
from pyhdf.SD import SD, SDC


OUTPUT_PATH = "outputs/seedability_map_real.png"


def resize_to_ctt(var, target_shape):
    return cv2.resize(
        var,
        (target_shape[1], target_shape[0]),
        interpolation=cv2.INTER_NEAREST
    )


def main():
    print("Loading MODIS cloud products...")

    FILE_PATH = "data/MOD06_L2.A2021196.0000.061.2021269014955.hdf"

    # -------------------------
    # DEBUG: Latitude / Longitude
    # -------------------------
    hdf = SD(FILE_PATH, SDC.READ)
    lat = hdf.select("Latitude")[:]
    lon = hdf.select("Longitude")[:]

    print("\n📍 Geographic coverage (from MODIS file):")
    print("Latitude  min/max:", np.nanmin(lat), np.nanmax(lat))
    print("Longitude min/max:", np.nanmin(lon), np.nanmax(lon))

    hdf.end()


    # -------------------------
    # 1. Load REAL MODIS data
    # -------------------------
    ctt = load_ctt()                    # (406,270) °C
    cot = load_cloud_thickness()        # (2030,1354)
    cwp = load_cloud_water_path()       # (2030,1354)
    phase = load_cloud_phase()          # (406,270)

    # -------------------------
    # 2. Resample to CTT grid
    # -------------------------
    cot = resize_to_ctt(cot, ctt.shape)
    cwp = resize_to_ctt(cwp, ctt.shape)

    h, w = ctt.shape

    # -------------------------
    # 3. DBZ proxy from water path
    # -------------------------
    wp_norm = np.nan_to_num(cwp, nan=0.0)
    dbz = np.clip((wp_norm / np.nanmax(wp_norm)) * 40, 0, 40)

    # -------------------------
    # 4. Seedability classification
    # -------------------------
    green, amber, gray = classify_seedability(
        ctt=ctt,
        depth=cot,
        dbz=dbz
    )

    # -------------------------
    # 5. Phase gating
    # 2 = ice (MODIS definition)
    # -------------------------
    ice_mask = (phase == 2)

    green[ice_mask] = False
    amber[ice_mask] = False
    gray[ice_mask] = True

    # -------------------------
    # 6. Generate color map
    # -------------------------
    output = create_color_map((h, w), green, amber, gray)
    cv2.imwrite(OUTPUT_PATH, output)

    print("✅ Seedability map generated using REAL MODIS data")
    print(f"Output saved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
