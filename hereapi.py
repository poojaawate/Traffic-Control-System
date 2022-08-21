import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
import numpy as np
import matplotlib.cm as cm
import requests
#import dill
from bs4 import BeautifulSoup
#from datetime import datetime
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import XML, fromstring, tostring
from supportFile import *

app_id = 'WeHEo2P2K8EG4bUYxyY4'
app_code = 'DA6FLaBn6Z8ybBH4JlVXwg'

def calculate_traffic(lat,lon):
 
    latmin,longmin,latmax,longmax=boundingBox(lat,lon,0.5)
    print(latmin)

    req = 'https://traffic.api.here.com/traffic/6.2/flow.xml?app_id='+app_id +'&app_code='+app_code+'&bbox='+str(latmin)+','+str(longmin)+';'+str(latmax)+','+str(longmax)+'&responseattributes=sh,fc'
    print(req)
    page = requests.get(req)

    #page = requests.get('https://traffic.api.here.com/traffic/6.2/flow.xml?app_id=WeHEo2P2K8EG4bUYxyY4&app_code=DA6FLaBn6Z8ybBH4JlVXwg&bbox=39.039696,-77.222108;38.775208, -76.821107&responseattributes=sh,fc')

    #page = requests.get('https://traffic.api.here.com/traffic/6.2/flow.xml?app_id=WeHEo2P2K8EG4bUYxyY4&app_code=DA6FLaBn6Z8ybBH4JlVXwg&bbox=18.305040617740406,73.8817301585201;18.39490178225959,73.97640544147991&responseattributes=sh,fc')

    soup = BeautifulSoup(page.text, "lxml")
    roads = soup.find_all('fi')

    print(len(roads))

    a1=[]
    loc_list_hv=[]
    lats=[]
    longs=[]
    sus=[]
    ffs=[]
    road_names=[]
    road_jf=[]
    road_avgSpeed=[]
    road_freeSpeed=[]
    c=0
    for road in roads:
        #for j in range(0,len(shps)):
        myxml = fromstring(str(road))
        #print(myxml)
        fc=5
        cn=0
        for child in myxml:
            #print(child.tag, child.attrib)
            if('fc' in child.attrib):
                fc=int(child.attrib['fc'])
            if('cn' in child.attrib):
                cn=float(child.attrib['cn'])
            if('su' in child.attrib):
                su=float(child.attrib['su'])
            if('ff' in child.attrib):
                ff=float(child.attrib['ff'])
            
        if((fc<=2) and (cn>=0.7)):            #consider only big roads(HIghways)
            shps=road.find_all("shp")
            tmc= road.find_all("tmc")
            cf=  road.find_all("cf")
            #print(tmc[0]['de'])              #road names
            road_names.append(tmc[0]['de'])

            #print(cf[0]['jf'])               #road jam factor 0(best) to 10(worst)
            road_jf.append(cf[0]['jf'])
            road_avgSpeed.append(cf[0]['su'])
            road_freeSpeed.append(cf[0]['ff'])

            for j in range(0,len(shps)):
                latlong=shps[j].text.replace(',',' ').split()
                #loc_list=[]
                la=[]
                lo=[]
                su1=[]
                ff1=[]
                
                for i in range(0,int(len(latlong)/2)):
                    loc_list_hv.append([float(latlong[2*i]),float(latlong[2*i+1]),float(su),float(ff)])
                    la.append(float(latlong[2*i]))
                    lo.append(float(latlong[2*i+1]))
                    su1.append(float(su))
                    ff1.append(float(ff))
                lats.append(la)
                longs.append(lo)
                sus.append(np.mean(su1))
                ffs.append(np.mean(ff1))

    #fig=plt.figure()
    plt.style.use('dark_background')
    #plt.plot(np.linspace(0,10,10),np.linspace(0,10,10))
    plt.grid(False)
    for i in range(0,len(lats)):
        if(sus[i]/ffs[i]<0.25):                                   #su:current avg speed, ff:free flow speed
            plt.plot(longs[i],lats[i], c='brown',linewidth=2)
        elif(sus[i]/ffs[i]<0.5):
            plt.plot(longs[i],lats[i], c='red',linewidth=2)
        elif(sus[i]/ffs[i]<0.75):
            plt.plot(longs[i],lats[i], c='yellow',linewidth=2)
        else:
            plt.plot(longs[i],lats[i], c='green',linewidth=2)
        #print(i)
    #plt.xlim(-77.055,-77.015)
    #plt.ylim(38.885,38.91)
    plt.axis('off')
    #plt.show()
    plt.savefig('static/images/traffic.jpg')
    plt.close()
    return(road_names,road_jf,road_avgSpeed,road_freeSpeed)

#roads,jf,avgspeed,freespeed=calculate_traffic(18.4536792,73.8563196)

#print(roads,jf,avgspeed,freespeed)