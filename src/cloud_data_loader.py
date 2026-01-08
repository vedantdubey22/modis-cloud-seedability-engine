from pyhdf.SD import SD, SDC
import numpy as np

FILE_PATH = "data/MOD06_L2.A2021196.0000.061.2021269014955.hdf"

# Open HDF file
hdf = SD(FILE_PATH, SDC.READ)

# -----------------------------
# 1. List all datasets (debug)
# -----------------------------
datasets = hdf.datasets()
print("Available datasets:")
print(datasets.keys())

# -----------------------------
# 2. Load Latitude & Longitude
# -----------------------------
lat = hdf.select('Latitude')[:]
lon = hdf.select('Longitude')[:]

# -----------------------------
# 3. Load Cloud Top Height (meters)
# -----------------------------
cth = hdf.select('Cloud_Top_Height')
cth_data = cth[:]

print("\nRaw CTH shape:", cth_data.shape)
print("Raw CTH min/max:", cth_data.min(), cth_data.max())

# -----------------------------
# 4. Handle fill values
# MODIS fill value = -32767
# -----------------------------
cth_data = np.where(cth_data == -32767, np.nan, cth_data)

print("Cleaned CTH min/max:", np.nanmin(cth_data), np.nanmax(cth_data))

# -----------------------------
# 5. North India mask
# (lat: 22–35, lon: 68–90)
# -----------------------------
north_india_mask = (
    (lat >= 22) & (lat <= 35) &
    (lon >= 68) & (lon <= 90)
)

cth_north_india = np.where(north_india_mask, cth_data, np.nan)

print("\nNorth India CTH:")
print("Shape:", cth_north_india.shape)
print("Min/Max:", np.nanmin(cth_north_india), np.nanmax(cth_north_india))

# -----------------------------
# 6. Close file
# -----------------------------
hdf.end()
