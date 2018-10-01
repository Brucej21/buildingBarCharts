#Quick Script that integrates PSMA's Beta APIs with ABS's SDMX at SA1.
#NOte that at time of writing there was limited coverage of at SA1 level from ABS's APIs and PSMA's Beta areas
#may also have limited coverage.

from geojson import MultiPolygon, Feature, FeatureCollection, dump
import requests, json # load Requests library, and JSON library for interpreting responses
#import credentials
import csv
import pprint
import time
import os

key = 'Insert PSMA Beta Key Here'
#get building
bl_url = 'https://api.psma.com.au/beta/v1/' 

PSMAheaders = {
        "Authorization": key,
        "Accept": "application/json"
    }


#===================================================================================================
def requestEngine(urlVar,inHeaders):   #GET generic request engine returns json.
    try:
        response = requests.get(urlVar, headers=inHeaders, verify=False)
        print (response)
        data = response.json()
        return data
        #data = json.loads(response.text) to pass back for csv parsing.
    except:
        print ("error in calling ") # + inHeaders + " services")


#=====================================================================
#Get point

try:
    pointlat, pointlong = input("Enter Latitude and Longitude with a space : (hit return to default:\
    -34.923 138.59)  ").split()

except:
    print("providing defualt values -34.954350,138.586377")
    pointlat, pointlong = (-34.955,138.586377) #(-34.954350,138.586377)


natcode = input("Please enter nationality code (eg Australian = 1101, Chinese = 6101 English = 2101: ")
if natcode == "":
    print("chinese has been defaulted")
    natcode = '6101'


print (pointlat)
print (pointlong)



#This is to give JS a point of focus. Have not got this working yet.

focuslatlong = {"lat_j": pointlat, "long_j": pointlong}


with open('../html/focuspoint.json', 'w+') as minif:
    dump(focuslatlong, minif)

#


#-------------------------------------------------------------------
#Get list of nearest buildings

bl_url_nearest = 'https://api.psma.com.au/beta/v1/buildings/nearest/?latLong=' + str(pointlat)\
                 + '%2C' + str(pointlong) + '&radius=100&page=1&perPage=100'
#datapy = requestEngine(include_all_url)
databuildlist = requestEngine(bl_url_nearest,PSMAheaders)
#response2 = requests.get(bl_url_nearest, headers=PSMAheaders, verify=False)
print (databuildlist)
#data2 = databuildlist.json()
#print (data2)



#------------------------
features = []


#  multi building workign need way to load to enable loop.



for item in databuildlist['data']:
    #buiilding id form up url
    building_id = item['buildingId']
    print(building_id)
    bl_url = 'https://api.psma.com.au/beta/v1/'
    include_all_url = bl_url + 'buildings/' + building_id + '/?include=averageEaveHeight%2Ccentroid\
    %2Celevation%2Cfootprint2d%2Cfootprint3d%2CmaximumRoofHeight%2CroofComplexity%2CroofMaterial%2CsolarPanel%2CswimmingPool'

    datapy = requestEngine(include_all_url,PSMAheaders)
    #print(datapy)
    # render geojosn

    try:
        maximumRoofHeight = datapy['maximumRoofHeight']
    except:
        maximumRoofHeight = 10

    print (maximumRoofHeight)

    #maximumRoofHeight = 500

    holdpoly = datapy['footprint2d']['coordinates']
    multipolygon = MultiPolygon(holdpoly)

    print("==================GET LINK based on first related address (assumption here!==============")
    addr = datapy['relatedAddressIds']

    print (addr)

    ### removed slice.... addr = addr[:1] # slices to first segment of list.

    print (addr)

    for add in addr:
        #go and get first address ASGS to get stats for
        #https: // api.psma.com.au / beta / v1 / addresses / addressID / asgsMain /
        get_address_url = bl_url + 'addresses/' + add + '/asgsMain/'
        print (get_address_url)
        dataAsgsID = requestEngine(get_address_url,PSMAheaders)
        print (dataAsgsID)
        v2011SA1 =  dataAsgsID['asgsMain']['2011']['sa1Id']
        print (v2011SA1)
        #Improvment here would be to cut out duplicate calls to ABS's SDMX.

        #ABS call----------------------------------------
        #
    abs_url = 'http://stat.data.abs.gov.au/sdmx-json/data/ABS_CENSUS2011_B08_SA1_SA/1.TOT+TOTP+1101+1102+6101+\
    3204+2303+2101+5201+2305+2306+3205+3304+7106+2201+3103+6902+4106+3206+3104+1201+1202+3307+3308+2102+3213+7115+\
    9215+3106+4907+5107+2103+OTH+Z.4.SA1.' + v2011SA1 + '.A/all?detail=Full&dimensionAtObservation=AllDimensions&startPeriod=2011&endPeriod=2011'

    ABSheaders = {
        # "Authorization": key,
        "Accept": "application/json"
    }
    dataABS = requestEngine(abs_url, ABSheaders)
    #response7 = requests.get(abs_url, headers=ABSheaders, verify=False)

    #data37 = response7.json()
    #data27 = json.loads(response7.text)
    print("dataABS")
    print(dataABS)
    request_dim_value5 = dataABS['structure']['dimensions']['observation'][1]['values'][4]['name']  # 'request_dim_value5': 'Chinese
    print (request_dim_value5)

    abs_data_load = dict()
    i = 0

    for item in dataABS['structure']['dimensions']['observation'][1]['values']:
        # print (type(item))
        print (item)
        for item2, value in item.items():
            # https://stackoverflow.com/questions/13603215/using-a-loop-in-python-to-name-variables
            abs_data_load["request" + str(i)] = value
            # ("request_dim_value" + str(i)) = value
            i = i + 1

    print ("---------------------OBSERVATIONS----------------------------------------")
    print ("obs")
    keyformat = '0:{0}:0:0:0:0:0'

    keyref = keyformat.format(24)

    obs = dataABS['dataSets'][0]['observations'][str(keyref)]

    print(obs)

    print("------------------------combined 2-----------------------------------------")
    i = 0

    for item in dataABS['structure']['dimensions']['observation'][1]['values']:
        # print (type(item))

        print("+++++++++++start  row            +++++++++++++")
        print (item)
        # print(item.name)
        # print ("here"+item.name.value)

        country = item['name']
        print(country)

        ref_id = item['id']
        print("ref_id below")
        print(ref_id)


        key2 = keyformat.format(i)
        measure = dataABS['dataSets'][0]['observations'][str(key2)]
        print (measure)
        persons = measure[0]
        print (persons)

        print (ref_id + "," + country + ", " + str(persons))

        if ref_id == 'TOTP':
            totalpeople = persons
            print("total people")
            print(totalpeople)
        if ref_id == natcode:
            countofnationality = persons
            countryoforigion = country


        i = i + 1





        #ABS --------------------------




    print ("addr +++++++++++++++++++++")
    print (addr)



    #print(multipolygon)
    print("==============")


    features.append(Feature(geometry=multipolygon, properties={"Country_Total": countofnationality, "MAX_HG2": totalpeople,\
                                                               "Country":countryoforigion }))

    # add more features...
    # features.append(...)

feature_collection = FeatureCollection(features)
    # dumps to where vizicities server can pick it up.
with open('../html/buildingradius.json', 'w+') as f:  #with open('../html/SouthAustralia.json', 'a') as f: or w or w+
    dump(feature_collection, f)







