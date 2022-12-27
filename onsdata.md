## ONS Datasets
The Office for National Statistics publishes datasets which are open source and usable in the public domain.  

Many of these datasets are avaialable directly from the ONS Website as downloadable CSV files.  

A good example is the August 2022 version of the National Statistics Postcode Lookup, which is a collection of CSV files that has a baseline dataset of Postcode geography details, containing reference codes that link to other lookup datasets.  Most of the other datasets in the collection contain descriptions of those codes, such as local authorities, district councils and many other political taxonomies.  
https://geoportal.statistics.gov.uk/datasets/ons::national-statistics-postcode-lookup-2021-census-august-2022-1/about

Other datasets are available as in-page lists that can be viewed in tabular form but can also be downloaded as CSV.  An example is the LAD (local authority districts) codes and matching names.  In this case the dataset is from December 2020.    
https://geoportal.statistics.gov.uk/datasets/ons::lad-dec-2020-names-and-codes-in-the-united-kingdom/explore?showTable=true

## Manual Searching vs Automation
The problem with these ONS datasets is that it is not optimal as we must:  
1. Find them on the webiste
2. Manualy download our selection

There is however, an option for automation.  This involves using software provided by *esri*, who are an American company that provides geographic information system software.  You can learn about what esri provide here:  
https://www.esri.com/en-us/about/about-esri/overview

The software that we will use is called **ArcGIS** which is a Geographical Information System.  The main usage of this tool is to manage geospatial information, but it is also used for more general purpose geography-related datasets.  
The ONS make their public datasets available through ArcGIS, which has a Python SDK.  

The documentation for using the SDK starts here:  
https://developers.arcgis.com/python/


## Prepare for ArcGIS
The easy way to use this SDK is to install the Anaconda environment on Windows and use the Conda package manager to install ArcGIS (not covered in this project).   

If you are on Linux (the default for this project) then you will have to perform some selective installs and find some specific versions of packages to enable compatibility with a standard Python environment.  
For python 3.9 see the below section to [setup ArcGIS in a standard Python environment](arcgis.md)

## Using ArcGIS SDK
Begin by identifying and obtaining references to some datasets.  There are 2 quick ways to do this.  

### Method 1
The first method is to get an ID reference to a specific dataset.  An example of this can be found by navigating to the 'data source' details in the download page for the *lad-dec-2020-names-and-codes* mentioned above.  
https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/LAD_Dec_2020_Names_and_Codes_in_the_United_Kingdom_2022/FeatureServer  
In this case the ID is shown as "Service ItemId: 3a7e23cc7c2f49a7953838a2e9a4ed1a".  

Use the ArcGIS content.get function to obtain the item reference.  
```
from arcgis import GIS

gisClient=GIS()
item = gisClient.content.get("3a7e23cc7c2f49a7953838a2e9a4ed1a")
```
The item identifies the ArcGIS resource.  
```
>>> item
<Item title:"LAD (Dec 2020) Names and Codes in the United Kingdom" type:Table Layer owner:ONSGeography_data>
```
As this is a single CSV file it is represented by ArcGIS as a data "table layer" type.
```
from arcgis.features import FeatureLayerCollection, Table
data_table = Table.fromitem(item)
```    
Converting the reference into a Table type results in the API that actually contains the data.  
```
>>> data_table
<Table url:"https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/LAD_Dec_2020_Names_and_Codes_in_the_United_Kingdom_2022/FeatureServer/0">
```
In order to read/download the data, the query function must be used.  In addition, the "as_df" query option returns the data as a Pandas dataframe.   
Note: it is the query function which actually retrieves data from the ArcGIS API service.
```
import pandas as pd

data_frame = data_table.query(as_df=True)
```
This results in a usable dataset within a Python program.  
```
>>> data_frame
     FID    LAD20CD               LAD20NM LAD20NMW
0      1  E06000001            Hartlepool     None
1      2  E06000002         Middlesbrough     None
2      3  E06000003  Redcar and Cleveland     None
3      4  E06000004      Stockton-on-Tees     None
4      5  E06000005            Darlington     None
..   ...        ...                   ...      ...
374  375  E08000027                Dudley     None
375  376  E08000028              Sandwell     None
376  377  E08000029              Solihull     None
377  378  E08000030               Walsall     None
378  379  E08000031         Wolverhampton     None

[379 rows x 4 columns]
```
  
### Method 2
The second method uses the content.search function to scan for dataset references.  There are several search options.    

An example that searches for a key word, an ArcGIS type and that limits the result set.  
```
search = gis.content.search(query="postcode", item_type="CSV Collection", max_items=8)
```
results in:
```
>>> for s in search:
...     print(s)
... 
<Item title:"metro_postcodes_20210907" type:CSV Collection owner:evenergi>
<Item title:"ONS UPRN Directory User Guide (April 2022)" type:CSV Collection owner:ONSGeography_data>
...
<Item title:"NHS Postcode Directory UK Full (February 2020)" type:CSV Collection owner:ONSGeography_data>
>>> 
```
Once you have a list, choose the item you require, either by an index or by some logic.
```
new_item = search[3]
```

Examples of other types of search using multiple query conditions:
```
# search by owner and type
gis.content.search(query="type:Feature Layer Collection, owner:ONSGeography_data", max_items=20)

# search using wildcards
search = gis.content.search(query="title:*Postcode*, type:Feature Layer, owner:ONSGeography_data", max_items=20)

# search using a more target specific wildcard
search = gis.content.search(query="title:Postcode to Output Area Hierarchy* AND owner:ONSGeography_data", max_items=10)
```

In the final search example, we are trying to find the *national-statistics-postcode-lookup-2021-census-august-2022* CSV collection which was mentioned at the top of this file.

The outputs of the search are:
```
>>> for s in search:
...     print(s)
... 
<Item title:"Postcode to Output Area Hierarchy with Classifications (May 2020) Multi-CSV Lookup in the UK" type:CSV Collection owner:ONSGeography_data>
<Item title:"Postcode to Output Area Hierarchy with Classifications (August 2018) Lookup in the UK" type:CSV Collection owner:ONSGeography_data>
<Item title:"Postcode to Output Area Hierarchy with Classifications (August 2020) Lookup in the UK" type:CSV Collection owner:ONSGeography_data>
<Item title:"Postcode to Output Area Hierarchy with Classifications (November 2021) Lookup in the UK" type:CSV Collection owner:ONSGeography_data>
<Item title:"Postcode to Output Area Hierarchy with Classifications (November 2018) Lookup in the UK" type:CSV Collection owner:ONSGeography_data>
<Item title:"Postcode to Output Area Hierarchy with Classifications (February 2021) Lookup in the UK" type:CSV Collection owner:ONSGeography_data>
<Item title:"Postcode to Output Area Hierarchy with Classifications (August 2019) Lookup in the UK" type:CSV Collection owner:ONSGeography_data>
<Item title:"Postcode to Output Area Hierarchy with Classifications (August 2022) Lookup in the UK" type:CSV Collection owner:ONSGeography_data>
<Item title:"Postcode to Output Area Hierarchy with Classifications (May 2022) Lookup in the UK" type:CSV Collection owner:ONSGeography_data>
<Item title:"Postcode to Output Area Hierarchy with Classifications (May 2020) Lookup in the UK" type:CSV Collection owner:ONSGeography_data>
```
The correct CSV collection is at index postion 7.
```
>>> for s in search:
...     s_txt = str(s)
...     if "(August 2022)" in s_txt:
...             new_item = s
... 
>>> new_item
<Item title:"Postcode to Output Area Hierarchy with Classifications (August 2022) Lookup in the UK" type:CSV Collection owner:ONSGeography_data> 
```

### Advanced Search
How many datasets does the ONS publish?
```
ons = "owner: ONSGeography_data"
gc = GIS()
count = gc.content.advanced_search(query=ons, return_count=True)
```

Search results expanded form.
```
res = gc.content.advanced_search(query=ons, max_items=20)
```
This adds additional metadata to the return result, with the actual search list as a dict within.
```
>>> res
{
'total': 4946, 
'start': 1, 
'num': 20, 
'nextStart': 21, 
'results': [
     <Item title:"1 no poverty" type:Hub Page owner:ONSGeography_data>, 
     <Item title:"10 reduced inequalities" type:Hub Page owner:ONSGeography_data>, 
     ...
     <Item title:"11 sustainable cities and communities" type:Hub Page owner:ONSGeography_data>, 
     <Item title:"7_Affordable" type:Image owner:ONSGeography_data>]
}
```
Return search results list in a dict format.
```
res = gc.content.advanced_search(query=ons, max_items=3, as_dict=True)

>>> print(res['results'][0])
{'id': '8de0665a43d148adaa2719387c5be9b5', 'owner': 'ONSGeography_data', 'created': 1511264803000, 'modified': 1512140472000, 'guid': None, 'name': None, 'title': '1 no poverty', 'type': 'Hub Page', 'typeKeywords': ['Hub', 'hubPage', 'JavaScript', 'Map', 'Mapping Site', 'Online Map', 'OpenData', 'selfConfigured', 'Web Map'], 'description': 'DO NOT DELETE OR MODIFY THIS ITEM. This item is managed by the ArcGIS Hub application. To make changes to this page, please visit https://hub.arcgis.com/admin/sites/ccf237e81cdd49778b679f2fcda07038/pages', 'tags': [], 'snippet': 'null', 'thumbnail': 'thumbnail/ago_downloaded.png', 'documentation': None, 'extent': [], 'categories': [], 'spatialReference': 'null', 'accessInformation': 'null', 'licenseInfo': 'null', 'culture': 'en-us', 'properties': None, 'advancedSettings': None, 'url': 'https://opendata.arcgis.com/admin/', 'proxyFilter': None, 'access': 'public', 'size': -1, 'subInfo': 0, 'appCategories': [], 'industries': [], 'languages': [], 'largeThumbnail': None, 'banner': None, 'screenshots': [], 'listed': False, 'numComments': 0, 'numRatings': 0, 'avgRating': 0, 'numViews': 237, 'scoreCompleteness': 61, 'groupDesignations': None, 'lastViewed': -1}
```
Search for a type of resource.
```
needed = "Table Layer"
res = gc.content.search(query=ons, item_type=needed, max_items=3)
```

Perform a search and convert the results into a Pandas dataframe.  Note: the scan variable must have the title as the first parameter or the search will return None.  
```
what = "title: (August 2022)"
scan = f'{what}, {ons}'
res_list = gc.content.advanced_search(query=scan, max_items=8, as_dict=True)['results']

resdf = pd.DataFrame(res_list)

>>> resdf['type'].value_counts()
CSV Collection    2
PDF               1
Name: type, dtype: int64

pd.set_option('max_colwidth', 250)
viewable = ['id','title','owner','type','access', 'url']

>>> resdf[viewable]
                                 id                                                                    title              owner            type  access
0  753037189b874508bfbbfca6fc90219c               Code History Database (August 2022) for the United Kingdom  ONSGeography_data  CSV Collection  public
1  d250dad5c9194cfcbd0975a659708188  Hierarchical Representation of UK Statistical Geographies (August 2022)  ONSGeography_data             PDF  public
2  be4a7ec642bb463886ab755ab29d103b             National Statistics Postcode Lookup (August 2022) User Guide  ONSGeography_data  CSV Collection  public
3  b1e0efef9de04859bc2a06146b0b57e2          National Statistics Postcode Lookup - 2011 Census (August 2022)  ONSGeography_data  CSV Collection  public
4  60484ad9611249b59f3644e92f37476d          National Statistics Postcode Lookup - 2021 Census (August 2022)  ONSGeography_data  CSV Collection  public
5  f731ed5b45874cfdbd24089b7ca07743                            National Statistics UPRN Lookup (August 2022)  ONSGeography_data  CSV Collection  public
6  13bf05e8b9bd4999bce0a5618b6fc89d            National Statistics UPRN Lookup 2021 User Guide (August 2022)  ONSGeography_data  CSV Collection  public
7  e420e2b384d749d795bea8d7be298ba3               National Statistics UPRN Lookup OA21 version (August 2022)  ONSGeography_data  CSV Collection  public
```
The same CSV collection we were searching for in Method 2 is in row 5.
```
item = gc.content.get('60484ad9611249b59f3644e92f37476d')
```

```
what = "title: National Statistics Postcode Lookup (August 2022)"
res_list = gc.content.advanced_search(query=what, max_items=20)

>>> for s in res_list['results']:
...     print(s)
... 
<Item title:"National Statistics Postcode Lookup (August 2022) User Guide" type:CSV Collection owner:ONSGeography_data>
<Item title:"National Statistics Postcode Lookup - 2011 Census (August 2022)" type:CSV Collection owner:ONSGeography_data>
<Item title:"National Statistics Postcode Lookup - 2021 Census (August 2022)" type:CSV Collection owner:ONSGeography_data>
<Item title:"National Statistics UPRN Lookup 2021 User Guide (August 2022)" type:CSV Collection owner:ONSGeography_data>
<Item title:"National Statistics UPRN Lookup User Guide (August 2022)" type:CSV Collection owner:ONSGeography_data>

item = res_list['results'][2]

>>> item
<Item title:"National Statistics Postcode Lookup - 2021 Census (August 2022)" type:CSV Collection owner:ONSGeography_data>

tb = Table.fromitem(item)
Traceback (most recent call last):
  File "/home/avr/projects/cucumber/.venv/cucumber/lib/python3.9/site-packages/arcgis/gis/__init__.py", line 11448, in __getitem__
    return dict.__getitem__(self, k)
KeyError: 'tables'

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/home/avr/projects/cucumber/.venv/cucumber/lib/python3.9/site-packages/arcgis/features/layer.py", line 3362, in fromitem
    return item.tables[table_id]
  File "/home/avr/projects/cucumber/.venv/cucumber/lib/python3.9/site-packages/arcgis/gis/__init__.py", line 11422, in __getattribute__
    if self["tables"] == None or self["tables"] == []:
  File "/home/avr/projects/cucumber/.venv/cucumber/lib/python3.9/site-packages/arcgis/gis/__init__.py", line 11452, in __getitem__
    return dict.__getitem__(self, k)
KeyError: 'tables'
```
..




