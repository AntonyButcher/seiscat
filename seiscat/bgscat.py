import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.mlab as ml
from mpl_toolkits.basemap import Basemap

import requests
from bs4 import BeautifulSoup


def bgs_events(lat0=50,lon0=1,rad=500,date1='2017-10-08',date2='2018-10-18'):
    ### Creates a pandas dataframe from the events within the specified period and location from the BGS website
    address='http://www.earthquakes.bgs.ac.uk/cgi-bin/get_events?'

    page = requests.get('%slat1=&lat2=&lon1=&lon2=&lat0=%s&lon0=%s&radius=%s&date1=%s&date2=%s&dep1=&dep2=&mag1=&mag2=&nsta1=&nsta2=&output=csv'%(address,lat0,lon0,rad,date1,date2))
    data = page.text
    soup = BeautifulSoup(data, "lxml")

    results=soup.get_text()

    file=open('events_tmp.csv','w')
    file.write(results)
    file.close()

    results_df=pd.read_csv('events_tmp.csv',names=['date', 'time', 'lat', 'lon', 'depth', 'ML', 'Nsta', 'RMS', 'intensity', 'locality','region'],skiprows=3)
    
    return results_df

def plot_locs(lat,lon,fig=None,marker='*',c='r'):
    """ Plots a map of the uk and locations from a panda dataframe """ 
    
    
    lat=lat.values
    lon=lon.values
    
    if fig==None:
        fig = plt.figure(figsize=(8,7))

    m = Basemap(projection='stere',width=1000000,height=1300000,\
                lat_ts=2,resolution='l',lat_0=55,lon_0=-4)

    m.drawcoastlines()
    m.drawcountries()
    m.drawmapboundary(fill_color='#99ffff')
    m.fillcontinents(color='#cc9966',lake_color='#99ffff',zorder=1,alpha=0.7)
    m.drawparallels(np.arange(50,80,2.5),labels=[1,0,0,0],fontsize=10)
    m.drawmeridians(np.arange(-10,10,5),labels=[0,0,0,1],fontsize=10)

    x,y=m(lon,lat)
    m.scatter(x,y,marker=marker,s=75,c=c,zorder=10)

    plt.tight_layout();
    
    return fig

def tr_write(tr,path,id,resp=False):
    """ Removes the instrument response, and exports data to a SAC format"""
    network=tr.stats.network
    if network=="":
        network="GB"    
    station=tr.stats.station
    channel=tr.stats.channel
    date=tr.stats.starttime
    
    if resp==True:
        resp_file='RESP/RESP.%s.%s.00.%s'%(network,station,channel)
        if not os.path.exists(resp_file):
            print('Response file could not be found')            
            pass
        else:
            pre_filt = (0.01,0.02,49.5,50)
            seedresp = {'filename': resp_file, 'date':date, 'units': 'DISP'} 
            tr.simulate(paz_remove=None, pre_filt=pre_filt, seedresp=seedresp)
    else:
        pass
    
    if network=="":
        network="xx"
        
    if not os.path.exists(path):
        os.makedirs(path)
        
    file="%s.%s.%s.%s.sac"%(network,station,id,channel)
    filename="%s%s"%(path,file)
    print(filename)
    tr.write(filename,format='SAC')
