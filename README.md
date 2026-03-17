# Logistics Route & Distance Calculator 🚚

A Python utility designed to automate the calculation of travel distances and durations for delivery routes (Romaneios). It processes geospatial data from Excel files, groups them by shipment ID, and integrates with the NextBillion.io Directions API to provide high-precision routing metrics.

### 🌟 Key Features
* **Sequential Route Processing:** Calculates distance (km) and time (seconds) between consecutive waypoints.
* **Automated Grouping:** Uses `pandas` to group data by shipment lists (`lista_35`), calculating total distance and time per group.
* **Geospatial Validation:** Automatically identifies and skips "Validation" points or rows with missing/zero coordinates to maintain data integrity.
* **API Integration:** Optimized requests using the NextBillion.io Directions API.
* **Progress Tracking:** Real-time feedback via `tqdm` progress bars and estimated time of completion.

### 🛠 Tech Stack
* **Language:** Python 3.x
* **Libraries:** `Pandas` (Data manipulation), `Requests` (API interaction), `Tqdm` (Progress tracking), `Openpyxl` (Excel I/O).
* **API:** NextBillion.io Directions API.

### 🚀 Usage
1. Place your input Excel file in the designated directory.
2. Update the `API_KEY` in the script.
3. Run the script:
   ```bash
   python route_calculator.py
