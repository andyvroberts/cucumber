import pandas as pd
from arcgis import GIS
from arcgis.features import FeatureLayerCollection, Table, FeatureCollection, FeatureLayer, FeatureSet


gisClient=GIS()
item = gisClient.content.get("3a7e23cc7c2f49a7953838a2e9a4ed1a")

data_table = Table.fromitem(item)

data_frame = data_table.query(as_df=True)



