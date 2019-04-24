import ee
import ee.mapclient
import datetime
ee.Initialize()

#shape generated in online code editor to filter out that we only want scotland
Scotland =ee.Geometry.Polygon([ [-8.832412990023954,54.955766854408964],
[0.17637607247604592,54.955766854408964],
[0.17637607247604592,59.24642577278162],
[-8.832412990023954,59.24642577278162],
[-8.832412990023954,54.955766854408964]])

#Sentinel 2 data filtered by date and region and select images with cloud cover <20%
corp = ee.ImageCollection("COPERNICUS/S2").filterDate(datetime.datetime(2018,6,22),datetime.datetime(2018,8,22)).filterBounds(Scotland).filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20))

#cloud mask function using the QA band to select pixels with no clouds
def maskCloud(image):
    QA = image.select('QA60')
    cloudBitMask = ee.Number(2).pow(10).int();
    cirrusBitMask = ee.Number(2).pow(11).int();
    mask = QA.bitwiseAnd(cloudBitMask).eq(0).And(QA.bitwiseAnd(cirrusBitMask).eq(0))
    return image.updateMask(mask).divide(10000)

#returns the NDVI of the image using B8 (NIR) and B2 (red)
def ndvi(image):
    return image.normalizedDifference(['B8', 'B2']);

#vis params
ndviParams = {'min': -0.5, 'max': 1, 'palette': ['306466','9cab68','cccc66','9c8448','6e462c']}

#centre on Edinburgh
ee.mapclient.centerMap(-3.195725712890635,55.95662062603667,9)

#add to map, applying mask, ndvi and a mean reducer
ee.mapclient.addToMap(corp.map(maskCloud).map(ndvi).reduce(ee.Reducer.median()), ndviParams)
