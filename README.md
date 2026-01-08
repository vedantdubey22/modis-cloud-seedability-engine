# MODIS Cloud Seedability Decision Engine

This project implements a **cloud seedability analysis pipeline** using  
**MODIS/Terra Level-2 cloud products (MOD06_L2)** obtained from **NASA Earthdata**.

The system processes real satellite swath data and classifies clouds into
different seedability categories based on physically meaningful cloud
microphysical parameters.

---

## 1. Objective

The objective of this project is to design a **rule-based decision engine**
that identifies potentially seedable clouds using satellite-derived parameters such as:

- Cloud Top Temperature (CTT)
- Cloud Optical Thickness (cloud depth proxy)
- Cloud Water Path (liquid water proxy)
- Cloud Phase (water / ice / mixed)

The output is a pixel-wise seedability classification map.

---

## 2. Data Source

- **Satellite:** MODIS (Moderate Resolution Imaging Spectroradiometer)
- **Platform:** Terra
- **Product:** MODIS/Terra Clouds Level-2 (MOD06_L2)
- **Format:** HDF4 (swath-based)
- **Source:** NASA Earthdata

Each MODIS Level-2 swath file contains:
- Cloud physical parameters
- Pixel-level latitude and longitude metadata

The geographic region is **implicitly defined by the satellite overpass**.
Latitude and longitude values are used to **verify spatial coverage**, not to request data.

---

## 3. Methodology

### 3.1 Data Ingestion
MODIS Level-2 datasets are read directly from the HDF file using `pyhdf`.
Each dataset is loaded as a two-dimensional array representing the satellite swath.

### 3.2 Parameter Processing
- **Cloud Top Temperature (CTT):** Converted to physical units using scale and offset.
- **Cloud Optical Thickness:** Used as a proxy for cloud vertical development.
- **Cloud Water Path:** Used as a proxy for liquid water availability.
- **Cloud Phase:** Ice-phase clouds are excluded from seeding consideration.

Products with different native resolutions are resampled to the
cloud-top temperature grid using nearest-neighbor interpolation.

### 3.3 Decision Logic
Clouds are classified using threshold-based rules:

- **Green (High Seedability):**
  - Cold cloud tops
  - Sufficient depth
  - Adequate liquid water

- **Amber (Marginal):**
  - Borderline temperature, depth, or water content

- **Gray (Not Seedable):**
  - Ice-phase clouds
  - Weak or unsuitable cloud conditions

### 3.4 Output Generation
The final output is a color-coded seedability map generated in
**MODIS swath coordinate space**.

---

## 4. Output Interpretation

- 🟩 **Green** — High seedability potential  
- 🟧 **Amber** — Marginal or uncertain conditions  
- ⬜ **Gray** — Not seedable (ice clouds or weak clouds)

The output is **not a geographic map projection**.
It represents pixel-wise decisions in satellite observation space.

---

## 5. Geographic Validation

Latitude and longitude arrays embedded in the MODIS file are used to:
- Verify that the satellite swath intersects the intended region
- Confirm regional relevance (e.g., North India)

The project does not perform map reprojection and is intended as a
**decision-engine prototype**, not a GIS visualization system.

---

## 6. Environment Setup

### 6.1 Clone Repository
```bash
git clone https://github.com/yourusername/seedability_engine.git
cd seedability_engine

### 6.2 create virtual environment
python -m venv venv
source venv/bin/activate        # Linux / Mac
venv\Scripts\activate           # Windows


### 6.3 Install dependencies
pip install -r requirements.txt
(If pyhdf fails to install via pip:)
    use (conda install -c conda-forge pyhdf)

## 7 
    1) Place a MODIS .hdf file inside the data/ directory.
    2) Update the file path in the source files if required.
    3) run (python src/main.py)

## 8 
    the output image will be shown in the "outputs" directory
