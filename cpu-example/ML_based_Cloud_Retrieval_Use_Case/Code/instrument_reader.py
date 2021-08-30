#instrument reader
#this package includes necessary functions for loading data from different instruments

import os
import numpy as np
from pyhdf.SD import SD, SDC
from pyhdf.HDF import *
from pyhdf.V import VD
from pyhdf.VS import *
from netCDF4 import Dataset
from math import *
import datetime
import h5py
from datetimerange import DateTimeRange

# function name: load_caliop_clayer1km_geoloc
# purpose: Read 1D Latitude/Longitude/UTC_Time from CALIOP Level-2 Cloud Layer 1km Product
# input: cal_1km_file = {FILENAME}
# output: Dictionary 'Longitude', 'Latitude', 'UTC_Time'
# usage: caliop_clayer1km_geo = load_caliop_clayer1km_geo(cal_1km_file='...')

def load_caliop_clayer1km_geoloc(cal_1km_file='',params={}):

    try:
        cal_1km_id = SD(cal_1km_file,SDC.READ)
        cal_lon = cal_1km_id.select('Longitude').get()
        cal_lat = cal_1km_id.select('Latitude').get()
        cal_igbp= np.squeeze(cal_1km_id.select('IGBP_Surface_Type').get())
        cal_snic= np.squeeze(cal_1km_id.select('Snow_Ice_Surface_Type').get())
        cal_utc = cal_1km_id.select('Profile_UTC_Time').get()
        cal_1km_id.end()

        cal_snic = cal_snic.astype(np.int16)
        cstart_date = int(cal_utc[0] + 20000000.)
        cend_date = int(cal_utc[-1]+ 20000000.)
        cstart_time = (cal_utc[0] - cstart_date + 20000000.) * 24. * 3600.
        cend_time = (cal_utc[-1] - cend_date + 20000000.) * 24. * 3600.
        cstart_dt = datetime.datetime.strptime(str(cstart_date),'%Y%m%d') + datetime.timedelta(seconds=cstart_time[0])
        cend_dt = datetime.datetime.strptime(str(cend_date),'%Y%m%d') + datetime.timedelta(seconds=cend_time[0])
        cal_range1 = cstart_dt.strftime("%Y-%m-%dT%H:%M:%S")
        cal_range2 = cend_dt.strftime("%Y-%m-%dT%H:%M:%S")
        cal_timerange = DateTimeRange(cal_range1, cal_range2)
        #print (cal_timerange)
        n_profile = cal_lon.shape[0]
        prof_s = 0
        prof_e = n_profile
        profile_dts = list() 
        profile_deltas = (cal_utc - cal_utc[0]) * 3600. * 24.
        for i_profile in range(0,n_profile):
            profile_dt = cstart_dt + datetime.timedelta(seconds=int(profile_deltas[i_profile]))
            profile_dts.append(profile_dt)

    except:
        cal_lon = np.full(1,-9999.99)
        cal_lat = np.full(1,-9999.99)
        cal_utc = np.full(1,-9999.99)
        cal_igbp= np.full(1,-1)
        cal_snic= np.full(1,-1)
        n_profile = 0
        profile_dts = list()

    return {'Longitude':cal_lon, 'Latitude':cal_lat, 'IGBP_Type':cal_igbp, 'Snow_Ice_Type':cal_snic, 'Profile_Datetime':np.asarray(profile_dts)}

# function name: load_viirs_vnp03_geoloc
# purpose: Read 2D Latitude/Longitude from VIIRS SNPP L1 Product
# input: vnp03_file = {FILENAME}
# output: Dictionary 'Longitude', 'Latitude', masked 2D array, and Granule starting, middle, and ending times
# usage: vnp03_geo = load_viirs_vnp03_geo(vnp03_file='...')

def load_viirs_vnp03_geoloc(vnp03_file='',params={}):

    vnp03_filename = os.path.basename(vnp03_file)
    vnp03_timeflag = vnp03_filename[vnp03_filename.find('.A')+2:vnp03_filename.find('.A')+14]
    sdt = datetime.datetime.strptime(vnp03_timeflag,'%Y%j.%H%M')
    mdt = sdt + datetime.timedelta(minutes=3, seconds=0)
    edt = sdt + datetime.timedelta(minutes=5, seconds=59)
    try:
        viirs_vnp03_id = Dataset(vnp03_file,'r')
        lat = viirs_vnp03_id['geolocation_data/latitude'][:]
        lon = viirs_vnp03_id['geolocation_data/longitude'][:]
        lsm = viirs_vnp03_id['geolocation_data/land_water_mask'][:]
    except:
        lat = -9999.99
        lon = -9999.99
        lsm = -1
    return {'Longitude':lon, 'Latitude':lat, 'LandSeaMask':lsm, 'Datetime':[sdt,mdt,edt]}


# May 4th 2021 update
# function name: load_modis_mod03_geoloc
# purpose: Read 2D Latitude/Longitude from MODIS L1 MO(Y)D03 Product
# input: mod03_file = {FILENAME}
# output: Dictionary 'Longitude', 'Latitude', masked 2D array, and Granule starting, middle, and ending times
# usage: mod03_geo = load_modis_mod03_geo(mod03_file='...')

def load_modis_mod03_geoloc(mod03_file='',params={}):

    mod03_filename = os.path.basename(mod03_file)
    mod03_timeflag = mod03_filename[mod03_filename.find('.A')+2:mod03_filename.find('.A')+14]
    sdt = datetime.datetime.strptime(mod03_timeflag,'%Y%j.%H%M')
    mdt = sdt + datetime.timedelta(minutes=2, seconds=30)
    edt = sdt + datetime.timedelta(minutes=4, seconds=59)
    try:
        modis_mod03_id = SD(mod03_file,SDC.READ)
        lat = modis_mod03_id.select('Latitude').get()
        lon = modis_mod03_id.select('Longitude').get()
        lsm = modis_mod03_id.select('Land/SeaMask').get()
    except:
        lat = -9999.99
        lon = -9999.99
        lsm = -1
    return {'Longitude':lon, 'Latitude':lat, 'LandSeaMask':lsm, 'Datetime':[sdt,mdt,edt]}


def save_caliop_dataset(calipso_file='',calipso_index='',selected_datasets='',save_file=''):

    ind = np.where(calipso_index>=0)
    if (len(ind)<=0):
        return
    fid = SD(calipso_file,SDC.READ)
    sid = h5py.File(save_file,'w')
     
    for selected_dataset in selected_datasets:
        #print (selected_dataset)
        dataset = np.squeeze(fid.select(selected_dataset).get())
        n_dim = len(dataset.shape)
        dims = dataset.shape
        if (n_dim==1):
            save_dataset = dataset[calipso_index[ind]]
        if (n_dim==2):
            save_dataset = dataset[calipso_index[ind],:]
        if (n_dim==3):
            save_dataset = dataset[calipso_index[ind],:,:]
        sid.create_dataset(selected_dataset,data=save_dataset)

    sid.close()
    fid.end()
    return

def save_viirs_dataset(viirs_file='',viirs_along='',viirs_cross='',selected_datasets='',save_file=''):

    ind = np.where(viirs_along>=0)
    if (len(ind)<=0):
        return
    fid = Dataset(viirs_file)
    sid = h5py.File(save_file,'w')
    for selected_dataset in selected_datasets:
        dataset = fid[selected_dataset][:]
        save_dataset = dataset[viirs_along[ind],viirs_cross[ind]]
        sid.create_dataset(selected_dataset,data=save_dataset)
    fid.close()
    sid.close()

    return
