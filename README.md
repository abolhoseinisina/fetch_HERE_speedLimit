This script reads a road spatial layer and fetches the speed limit for each section of it from HERE API. Here is the instruction to use this script:
1. Install python dependencies: `pip install -r requirements.txt`
2. Get HERE API Key from (https://platform.here.com/)
3. Enter your API Key in the script `HERE_API_KEY`.
4. Place your spatial layer in shapefile, JSON, GeoJSON, or KML format in the data folder.
5. Modify the `ROAD_LAYER_PATH` variable in the script with the name of your spatial layer.
6. Run the script: `python main.py`
