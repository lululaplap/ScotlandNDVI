import ee
import ee.mapclient

import datetime

ee.Initialize()

Scotland =ee.Geometry.Polygon([ [-8.832412990023954,54.955766854408964],
[0.17637607247604592,54.955766854408964],
[0.17637607247604592,59.24642577278162],
[-8.832412990023954,59.24642577278162],
[-8.832412990023954,54.955766854408964]])#shape generated in online code editor to filter out that we only want scotland

corp = ee.ImageCollection("COPERNICUS/S2").filterDate(datetime.datetime(2017,6,1),datetime.datetime(2017,6,29)).filterBounds(Scotland).select(['QA60','B1','B2','B3','B4','B8'])



def maskCloud(image):
    QA = image.select('QA60')
    cloudBitMask = ee.Number(2).pow(10).int();
    cirrusBitMask = ee.Number(2).pow(11).int();
    mask = QA.bitwiseAnd(cloudBitMask).eq(0).And(QA.bitwiseAnd(cirrusBitMask).eq(0))
    return image.updateMask(mask).divide(10000)
#print(corp.map(maskCloud))



ee.mapclient.centerMap(-3.195725712890635,55.95662062603667,6)
# Select the red, green and blue bands.
def ndvi(image):
    return image.normalizedDifference(['B2', 'B8']);

ndviParams = {'min': -1, 'max': 1, 'palette': ['blue', 'white', 'green']}
ee.mapclient.addToMap(corp.map(maskCloud).map(ndvi).mean(), ndviParams)
# ee.mapclient.addToMap(image, {'gain': [1.4, 1.4, 1.1]})
# ee.mapclient.addLayer(corp.select(['B2','B3','B4']).mosaic(),{},'k')
