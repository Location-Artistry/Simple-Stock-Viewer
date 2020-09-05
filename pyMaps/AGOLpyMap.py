from pathlib import Path
import sys
import os
import datetime as dt
import pandas as pd
from arcgis.gis import GIS, Item
from arcgis.env import active_gis
from arcgis.features import FeatureLayerCollection
from arcgis.mapping import WebMap
from IPython.display import display
import getpass
from pathlib import Path
from zipfile import ZipFile
import streamlit as st
import numpy as np

# Collection of all ArcGIS Python API Helper Functions
# user login functions, ask if user would like additional logins
def userLogin():
    #userID = input(f'ArcGIS Online USER ID: ')
    #passWord = getpass.getpass('PASSWORD: ')
    userID = 'ekerney_nhbptribe'
    passWord = 'nx5b3049'
    try:
        global gis
        gis = GIS("https://www.arcgis.com", userID, passWord)
        print(f'SUCCESS - CONNECTED TO: {gis.users.me.username} ACCOUNT as <gis>')
        print(gis)
        #addUsers = input(f'Additional User Login(YES/NO)? ')
        addUsers = 'NO'
        if addUsers.upper() == 'YES':
            additionalUserLogin()
        else:
            print(f'YOU MAY NOW PROCEED...')
    except:
        print(f'ERROR DID NOT CONNECT TO: {userID}')

def additionalUserLogin():
    userID = input(f'ArcGIS Online USER ID: ')
    passWord = getpass.getpass('PASSWORD: ')
    try:
        global gis2
        gis2 = GIS("https://www.arcgis.com", userID, passWord)
        print(f'SUCCESS - CONNECTED TO: {gis2.users.me.username} ACCOUNT as <gis2>')
        print(gis2)
    except:
        print(f'ERROR DID NOT CONNECT TO: {userID}')

# get list of all owner AGOL items, print list with title, id, type, and categories
def getUserContent(gisInfo):
    try:
        my_content = gisInfo.content.search(query="owner:" + gisInfo.users.me.username, item_type="", max_items=200)
        for x in my_content:
            strMod = str(x.modified)
            stampInt = int(strMod[0:10])
            print(f'{x.title} - {x.id} - {x.type} - {x.categories} - {dt.datetime.fromtimestamp(stampInt)}')
    except:
        print('ERROR could not get user content')

# Clone item using id of item passed to function
def cloneItem(gisInfo, gisInfo2, cloneID):    
    try:
        itemToClone = gisInfo.content.get(cloneID)
        print('Cloning:' + itemToClone.title + ' - ' + itemToClone.id + ' -',itemToClone.type)
        clonedItem = gisInfo2.content.clone_items(items=[itemToClone])
        print(f'Cloned Item: {clonedItem[0]}')
        #return clonedItem
    except:
        print('ERROR Could Not Clone')

# updated searchByKeywords, returns LIST of items 8-14-2020
def searchByKeywords(gisInfo, searchKeywords):
    try:
        searchContent = gisInfo.content.search(query=f'{searchKeywords}', item_type='', max_items=50)
        x = 0
        for z in searchContent:
          strMod = str(z.modified)
          stampInt = int(strMod[0:10])
          print(f'{x} - {z.title} - {z.id} - {z.type} - {z.categories} - {dt.datetime.fromtimestamp(stampInt)}')
          x += 1
        return searchContent
    except:
        print('ERROR Search not Successful')

# find item by keywords and display visual card
def searchByKeyViz(gisInfo, searchKeywords):
    try:
        searchContent = gisInfo.content.search(query=f'{searchKeywords}', item_type='', max_items=50)
        for z in searchContent:
            print(f'title: {z.title} - itemID: {z.id} - type: {z.type}')
            display(z)
    except:
        print('ERROR Search not Successful')
        
# return all keys and values for item when passed itemID string
def getItemKeysValues(gisInfo, idString):
    try:
        getFeature = gisInfo.content.get(idString)
        for key, value in getFeature.items():
            print(key,': ', value)
    except:
        print('ERROR GET Keys/Values not Successful')
        
# takes itemID and gets and returns layerObject if exist, otherwise 'no layers found'
def getLayers(gisInfo, idString):
    getFeature = gisInfo.content.get(idString)
    try:
        featureLayers = getFeature.layers
        z = 0 
        for x in featureLayers:
            print(f'Layer {z}: {x}')
            z += 1
    except:
        print('no layers found')
    return featureLayers

# supply feature layer itemID, and the layer number to display table head 
def getLayerTable(gisInfo, idString, layerNum):
    try:
        layerOutput = getLayers(gisInfo, idString)
        queryLayer = layerOutput[layerNum].query()
        display(queryLayer.sdf.head())
    except:
        print('ERROR no Layers Found')
        
# delete item by itemID
def deleteItem(gisInfo, idString):
    itemToDelete = gisInfo.content.get(idString)
    display(itemToDelete)
    delQuest = input(f'Are you sure you want to delete: {itemToDelete.title}')
    try:
        if delQuest.upper() == 'YES':
            print(f'DELETING: {itemToDelete.title}')
            itemToDelete.delete()
        else:
            print(f'NOT DELETING: {itemToDelete.title}')
    except:
        print(f'ERROR failed to DELETE: {itemToDelete.title}')

# delete multiple items by searchByKeywords() returned LIST 8-14-2020
def delMultiple(gisInfo, itemList):
  try:
    print('List of Items to be Deleted: ')
    for z in itemList:
          strMod = str(z.modified)
          stampInt = int(strMod[0:10])
          print(f'{z.title} - {z.id} - {z.type} - {z.categories} - {dt.datetime.fromtimestamp(stampInt)}')
    delQuest = input(f'SURE YOU WANT TO DELETE THESE?!?!?')
    if delQuest.upper() == 'YES':
      for z in itemList:
          print(f'DELETING {z.title}')
          itemToDelete = gisInfo.content.get(z.id)
          itemToDelete.delete()
      print('<FINISHED DELETION PROCESS>')
    else:
      print(f'NOT DELETING!')
  except:
      print(f'ERROR failed to DELETE: {itemToDelete.title}')

# List all user Dashboards and Dashboard Webmmaps
def ListAllDashWebmaps(gisInfo):
  source_admin_inventory = get_user_items(gisInfo, gisInfo.users.me)
  x = 0
  try:
    for dashboard in source_admin_inventory['Dashboard']:
        print(x, dashboard)
        dashWebmap = get_dash_wm(gisInfo, dashboard)
        print(dashWebmap)
        x += 1
  except:
    print("ERROR COULD NOT LIST DASHBOARDS") 

# generic function update targetLayer Features based on Table Records
def updateLayFeatFromTable(gisInfo, targetLayerID, matchAttrib, targetAttrib, sourceAttrib):
  try:
    getLayers = gisInfo.content.get(targetLayerID)
    targetLayer = getLayers.layers
    layerFeatures = targetLayer[0].query()
    sourceTable = getLayers.tables
    tableFeatures = sourceTable[0].query()
    for tableFeature in tableFeatures:
      tableFeatureID = tableFeature.attributes[matchAttrib]
      for layerFeature in layerFeatures:
        layerFeatureID = layerFeature.attributes[matchAttrib]
        if tableFeatureID == layerFeatureID:
          targetValue = tableFeature.attributes[sourceAttrib]
          layerFeature.set_value(targetAttrib, targetValue)
          print(f'feature: {layerFeatureID} from tableFeature: {tableFeatureID} set {targetAttrib} as: {targetValue}')
    layerEdits = targetLayer[0].edit_features(updates=layerFeatures)
    editCounter = 0
    for edits in layerEdits['updateResults']:
      editCounter+=1
    print(f'updated {getLayers.title} with {editCounter} edits from {getLayers.tables[0]}')
  except:
    print(f'update features failed for {getLayers.title}')
  
# generic function update targetLayer Features based on Table Record, adds break list for parameter categories mapping/analysis
# 8-14 Updated to screen for sampling records with blank values: 'None'
def updateLayFeatFromTableBreaks(gisInfo, targetLayerID, matchAttrib, targetAttrib, sourceAttrib, breaksList):
  try:
    getLayers = gisInfo.content.get(targetLayerID)
    targetLayer = getLayers.layers
    layerFeatures = targetLayer[0].query()
    sourceTable = getLayers.tables
    tableFeatures = sourceTable[0].query()
    for tableFeature in tableFeatures:
      #tableFeatureID = tableFeature.attributes[matchAttrib]
      print(tableFeature.attributes['WATER_TEMP'] is None)
      if (tableFeature.attributes['WATER_TEMP'] is None) != True:
        tableFeatureID = tableFeature.attributes[matchAttrib]
        for layerFeature in layerFeatures:
          layerFeatureID = layerFeature.attributes[matchAttrib]
          if tableFeatureID == layerFeatureID:
            targetValue = tableFeature.attributes[sourceAttrib]
            x = 1
            for breakVal in breaksList:
              if targetValue > breakVal:
                print('none')
              else:
                layerFeature.set_value(targetAttrib, x)
                print(f'feature: {layerFeatureID} from tableFeature: {tableFeatureID} set {targetAttrib}: {targetValue} as: {x}')
                break
              x+=1
    layerEdits = targetLayer[0].edit_features(updates=layerFeatures)
    editCounter = 0
    for edits in layerEdits['updateResults']:
      editCounter+=1
    # hide REST infor for updated layers and tables
    # print(f'updated {getLayers.title} with {editCounter} edits from {getLayers.tables[0]}')
    print(f'updated {getLayers.title} with {editCounter} edits')
  except:
    print(f'update features failed for {getLayers.title}')

# download Feature Layer data from AGOL, unzip contents to folder with item.title name
# Export Formats: Shapefile | CSV | File Geodatabase | Feature Collection | GeoJson | Scene Package | KML | Excel
def downloadItem(gisInfo, idString):
    try:
        downloadData = gisInfo.content.get(idString)
        dataPath = Path('/data')
        print(f'Downloading: {downloadData.title} to {dataPath} directory')
        if not dataPath.exists():
          dataPath.mkdir()
        # this portion for feature service
        downloadExport = downloadData.export(title=downloadData.title, export_format="CSV")
        zipPath = downloadExport.download(save_path=dataPath)
        # preparing to extract files to directory with item.title name
        #zipPath = downloadData.download(save_path=dataPath)
        extractPath = dataPath.joinpath(downloadData.title)
        # extract files to /data directory
        zipFiles = ZipFile(zipPath)
        zipFiles.extractall(path=extractPath)
        print(f'list of Files extracted to: {extractPath}')
        print(list(file.name for file in extractPath.glob('*')))
    except:
        print('ERROR DOWNLOAD did not workings!')

def searchItem(gisInfo, searchKeywords, itemType):
    try:
        searchContent = gisInfo.content.search(query=f'{searchKeywords}', item_type=itemType, max_items=25)
        if itemType == 'Feature Service':
            x = 0
            print(f'<Search Query for {searchKeywords}>')
            for z in searchContent:
                strMod = str(z.modified)
                stampInt = int(strMod[0:10])
                print(f'{x} - {z.title} - {z.id} - {z.type} - {z.categories} - {dt.datetime.fromtimestamp(stampInt)}')
                x += 1
            layInd = int(input(f'Index of selected Feature Layer: '))
            addLayer = gisInfo.content.get(searchContent[layInd].id)
            return addLayer
        elif itemType == 'Web Map':
            x = 0
            print(f'<Search Query for {searchKeywords}>')
            for z in searchContent:
                strMod = str(z.modified)
                stampInt = int(strMod[0:10])
                print(f'{x} - {z.title} - {z.id} - {z.type} - {z.categories} - {dt.datetime.fromtimestamp(stampInt)}')
                x += 1
            layInd = int(input(f'Index of selected Feature Layer: ')) or 'NONE'
            #print(searchContent[layInd])
            mapReturn = searchContent[layInd]
            return mapReturn
    except:
        print('ERROR Search not Successful')
        
def quickMap():
  mapType = input(f'(YES) for QuickMap (NO) for Existing: ')
  if mapType.upper() == 'NO':
    mapSize = ['480px','720px','960px']
    print(f'<You entered {mapType} please login below>')
    userLogin() 
    mapKeywords = input(f'Name of WebMap to Search for: ') or ''
    mapObj = searchItem(gis,mapKeywords,'Web Map')
    map = gis.map(mapObj)
    sizeIn = int(input(f'MAP SIZE (0)SMALL (1)MEDIUM (2)HUGE: '))
    map.layout.height = mapSize[sizeIn]
    display(map)
  else:
    print(f'<You entered {mapType} Opening QuickMap>')
    mapList = ['topo','hybrid','streets','dark-gray','terrain']
    mapDimen = ['2D','3D']
    mapSize = ['480px','720px','960px']
    mapLoc = input(f'Location (default=Michigan): ') or 'Michigan'
    mapBaseNum = input(f'Basemap (default=topo (1=hybrid,2=streets,3=dark-gray,4=terrain): ') or 0
    mapDimIn = input(f'ENTER (1) for 3D Map: ') or 0
    atlasLayers = input(f'Layers from Living Atlas(Enter for None): ') or 'NONE'
    gisNone = GIS()
    map = gisNone.map(mapLoc)
    map.basemap = mapList[int(mapBaseNum)]
    if atlasLayers != 'NONE':
        layerDisplay = searchItem(gisNone, atlasLayers,'Feature Service')
        for layrs in layerDisplay.layers:
            map.add_layer(layrs)
    map.mode = mapDimen[int(mapDimIn)]
    sizeIn = int(input(f'MAP SIZE (0)SMALL (1)MEDIUM (2)HUGE: '))
    map.layout.height = mapSize[sizeIn]
    display(map)

# Delete all features from selected Feature Service, may need more debugging
def delAllFeatures(gisInfo, idString):
    delFeatures = gisInfo.content.get(idString)
    display(delFeatures)
    delQuest = input(f'Are you sure you want to delete all the feature in? {delFeatures.title}')
    try:
        if delQuest.upper() == 'YES':
            print('in loop')
            print(f'DELETING ALL FEATURES IN: {delFeatures.title}')
            featDelRes = []
            targetLayer = delFeatures.layers
            layerFeatures = targetLayer[0].query()
            for feature in layerFeatures:
              #print(f'features: {feature.attributes}')
              featDelRes.append(targetLayer[0].edit_features(deletes=str(feature.attributes['objectid'])))
            return featDelRes
        else:
            print(f'NOT DELETING: {delFeatures.title}')
    except:
        print(f'ERROR failed to DELETE: {delFeatures.title}')

# *******ESRI pre-made helper functions********
def is_hosted(gisInfo, item):
    return [keyword for keyword in item.typeKeywords if "Hosted" in keyword] 

# Prints all layers in a webmap, very handy
def print_webmap_inventory(gisInfo, wm):
    wm_obj = WebMap(wm)
    print(f"{wm_obj.item.title}\n{'-'*100}")
    for wm_layer in wm_obj.layers:
        try:
            if is_hosted(Item(gisInfo, wm_layer['itemId'])):
                print(f"{' '*2}{wm_layer['title']:40}HOSTED{' ':5}"
                      f"{wm_layer['layerType']:20}{dict(wm_layer)['itemId']}")
            else:
                print(f"{' '*2}{wm_layer['title']:40}other{' ':6}"
                      f"{wm_layer['layerType']:20}{wm_layer.id}") 
        except:
            print(f"{' '*2}{wm_layer['title']:40}other{' ':6}"
                  f"{wm_layer['layerType']:20}{wm_layer.id}")
    print("\n")

def get_webmap_list(wm):
    wm_obj = WebMap(wm)
    wmList = []
    print(f"{wm_obj.item.title}\n{'-'*100}")
    for wm_layer in wm_obj.layers:
        # print(wm_layer.itemId)
        wmList.append(wm_layer.itemId)
    return(wmList)
    
def displayWebmapLayers(gisInfo, idList):
    for id in idList:
        displayLayer = gisInfo.content.get(id)
        display(displayLayer)

def get_user_items(gisInfo, user):
    user_inventory = {}
    user_items = gisInfo.content.search(query=f"* AND owner:{user.username}", 
                                           max_items=500)
    for item in user_items:
        if item.type not in user_inventory:
            user_inventory[item.type] = [i 
                                         for i in user_items 
                                         if i.type == item.type]
    return user_inventory

def print_user_inventory(inventory):
    for itype, ilist in inventory.items():
        try:
            print(f"{itype}\n{'-'*50}")
            for i in ilist:
                print(f"{' ':3}{i.title:50}")
            print("\n")
        except Exception as e:
            print(f"\t\tOperation failed on: {i.title}")
            print(f"\t\tException: {sys.exc_info()[1]}")
            continue
            
def get_dash_wm(gisInfo, dash):
    return [gisInfo.content.get(widget['itemId']) 
            for widget in dash.get_data()['widgets'] 
            if widget['type'] == "mapWidget"]

# find item by keywords and display visual card
def searchByKeyViz(gisInfo, searchKeywords):
    try:
        searchContent = gisInfo.content.search(query=f'{searchKeywords}', item_type='', max_items=50)
        for z in searchContent:
            st.write(f'title: {z.title} - itemID: {z.id} - type: {z.type}')
            #st.write(z)
    except:
        print('ERROR Search not Successful')

userLogin()
#searchByKeyViz(gis, 'water data 2020')

st.title('ArcGIS Python API QuickMap')
st.write("Here's our first attempt at using data to create a table:")
st.write(pd.DataFrame({
    'first column': [1, 2, 3, 4],
    'second column': [10, 20, 30, 40]
}))
df = pd.DataFrame({'col1': [1,2,3]})
df  # <-- Draw the dataframe
map_data = pd.DataFrame(
    np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
    columns=['lat', 'lon'])

#st.map(map_data)
#quickMap()
searchKeywords = 'water data 2020'
searchContent = gis.content.search(query=f'{searchKeywords}', item_type='', max_items=50)
#for z in searchContent:
    #st.write(f'title: {z.title} - itemID: {z.id} - type: {z.type}')    
#    display(z)

#mapList = ['topo','hybrid','streets','dark-gray','terrain']
#mapDimen = ['2D','3D']
##mapSize = ['480px','720px','960px']
#mapLoc = input(f'Location (default=Michigan): ') or 'Michigan'
#mapBaseNum = input(f'Basemap (default=topo (1=hybrid,2=streets,3=dark-gray,4=terrain): ') or 0
#mapDimIn = input(f'ENTER (1) for 3D Map: ') or 0
#atlasLayers = input(f'Layers from Living Atlas(Enter for None): ') or 'NONE'
gisNone = GIS()
map = gisNone.map('Michigan')
#map.basemap = mapList[int(mapBaseNum)]
map
#st.write(map)
