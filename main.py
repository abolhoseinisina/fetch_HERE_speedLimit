import json
import numpy
import requests
import geopandas
from tqdm import tqdm

HERE_API_KEY = ''
ROAD_LAYER_PATH = 'data/LRS_HIGHWAY_NETWORK_2018.kml'

def readSpatialLayer(file_path: str):
    if not any(file_path.endswith(extension) for extension in ('.shp', '.json', '.geojson', '.kml')):
        raise ValueError('The spatial layer must be in shapefile, kml, json, or geojson format with a valid geometry.')

    spatial_layer = geopandas.read_file(file_path).to_crs(4326)
    if "SpeedLimit" not in spatial_layer.columns:
        spatial_layer["SpeedLimit"] = numpy.nan
    
    return spatial_layer

def writeSpatialLayerAsShapefile(geodataframe: geopandas.GeoDataFrame, outputfileName: str):
    geodataframe.to_file(outputfileName)

def fetchSpeedLimitFromHERE(line, midpoint):
    if not numpy.isnan(line['SpeedLimit']):
        return int(line['SpeedLimit'])

    url = f'https://router.hereapi.com/v8/routes?destination={midpoint.y},{midpoint.x}&origin={midpoint.y},{midpoint.x}&return=polyline&transportMode=car&spans=maxSpeed,names&apikey={HERE_API_KEY}'
    results = requests.get(url)
    if results.status_code == 200:
        results = json.loads(results.content)
        if results['routes'] is not None and results['routes'][0]['sections'] is not None and results['routes'][0]['sections'][0]['spans'] is not None and 'maxSpeed' in results['routes'][0]['sections'][0]['spans'][0]:
            speed = results['routes'][0]['sections'][0]['spans'][0]['maxSpeed']
            return int(speed * 3.6)
    
    elif results.status_code == 401 or results.status_code == 403:
        raise ValueError('You are not authorized to use this API. Check if you have a valid HERE API KEY.')
    
    else:
        print(f'Error in getting speed limit for a road segment: {results.content}')

def main():
    road_layer = readSpatialLayer(ROAD_LAYER_PATH)
    road_layer_midpoints = road_layer.representative_point()
    print(f'{len(road_layer.index)} road segments are loaded!')
    
    speeds = []
    for index, road_section in tqdm(road_layer.iterrows(), total=road_layer.shape[0], ncols=100, desc='Fetching speed limits'):
        speed = fetchSpeedLimitFromHERE(road_section, road_layer_midpoints.iloc[index])
        speeds.append(speed)

    road_layer['SpeedLimit'] = speeds
    writeSpatialLayerAsShapefile(road_layer, ROAD_LAYER_PATH)

if __name__ == '__main__':
    main()