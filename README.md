This script reads a road spatial layer and retrieves the speed limit for each road section using the HERE API. To use this script:
1. Install required Python dependencies: `pip install -r requirements.txt`
2. Obtain a HERE API key from `https://platform.here.com/`
3. Enter your API key in the script by setting the `HERE_API_KEY` variable.
4. Place your spatial layer (in Shapefile, JSON, GeoJSON, or KML format) in the `data` folder.
5. Update the `ROAD_LAYER_PATH` variable in the script to match your spatial layer’s filename. If not specified, the sample file `LRS_HIGHWAY_NETWORK_2018.kml` will be used.
6. Run the script: `python main.py`
