import numpy as np
from pvlib import atmosphere
from pvlib.tools import datetime_to_djd, djd_to_datetime
from math import *

def target_distance(target_lat, target_lon, granule_lat, granule_lon):
    # approximate radius of earth in km
    earth_radius = 6373.0

    shape = granule_lat.shape
    n_element = granule_lat.size

    locs_1 = np.deg2rad([[target_lat,target_lon]])

    granule_locs = np.zeros([n_element,2])
    granule_locs[:,0] = np.reshape(granule_lat,(n_element))
    granule_locs[:,1] = np.reshape(granule_lon,(n_element))

    locs_2 = np.deg2rad(granule_locs)

    lat_dif = (locs_1[:,0][:,None]/2 - locs_2[:,0]/2)
    lon_dif = (locs_1[:,1][:,None]/2 - locs_2[:,1]/2)

    np.sin(lat_dif, out=lat_dif)
    np.sin(lon_dif, out=lon_dif)

    np.power(lat_dif, 2, out=lat_dif)
    np.power(lon_dif, 2, out=lon_dif)

    lon_dif *= ( np.cos(locs_1[:,0])[:,None] * np.cos(locs_2[:,0]) )
    lon_dif += lat_dif
    lon_dif[lon_dif>1.0] = 1.0

    np.arctan2(np.power(lon_dif,.5), np.power(1-lon_dif,.5), out = lon_dif)
    lon_dif *= ( 2 * earth_radius )

    distance = np.reshape(lon_dif,shape)

    return distance

def targets_distance(target_lats, target_lons, granule_lat, granule_lon):

    # approximate radius of earth in km
    earth_radius = 6373.0

    shape = granule_lat.shape
    n_element = granule_lat.size
    n_target = len(target_lats)

    granule_locs = np.zeros([n_element,2])
    granule_locs[:,0] = np.reshape(granule_lat,(n_element))
    granule_locs[:,1] = np.reshape(granule_lon,(n_element))

    locs_1 = np.zeros([n_target,2])
    locs_1[:,0:1] = np.deg2rad(target_lats)
    locs_1[:,1:2] = np.deg2rad(target_lons)

    distance = np.zeros([shape[0], shape[1], n_target])
    locs_2 = np.deg2rad(granule_locs)

    lat_dif = (locs_1[:,0][:,None]/2 - locs_2[:,0]/2)
    lon_dif = (locs_1[:,1][:,None]/2 - locs_2[:,1]/2)

    np.sin(lat_dif, out=lat_dif)
    np.sin(lon_dif, out=lon_dif)

    np.power(lat_dif, 2, out=lat_dif)
    np.power(lon_dif, 2, out=lon_dif)

    lon_dif *= ( np.cos(locs_1[:,0])[:,None] * np.cos(locs_2[:,0]) )
    lon_dif += lat_dif
    lon_dif[lon_dif>1.0] = 1.0
    
    np.arctan2(np.power(lon_dif,.5), np.power(1-lon_dif,.5), out = lon_dif)
    lon_dif *= ( 2 * earth_radius )

    distance = np.reshape(np.transpose(lon_dif), (shape[0],shape[1],n_target) )

    return distance


def geostationary_view(sat_lon,orbit_radius,target_lats,target_lons):

    #input:
    #sat_lon: satellite longitude (-180 ~ 180, in degree)
    #orbit_radius: distance between satellite and center of the Earth (in km, always close to ~42,000km)
    #target_lats: target latidues (in degree, array)
    #target_lons: target longitudes (-180 ~ 180, array)

    #output:
    #sat_vzas: satellite viewing zenith angles (in degree, array)
    #sat_vaas: satellite viewing azimuthal angles (in degree, array)

    #convert target lat/lon to 1D vector
    n_dims = np.asarray(target_lats).ndim  
    dims = np.zeros(n_dims,np.int)
    tup = np.asarray(target_lats).shape
    dims = np.asarray(tup)
    #print (dims)

    target_lats_use = np.asarray(target_lats).flatten()
    target_lons_use = np.asarray(target_lons).flatten()

    #check input:
    if (sat_lon>180.0):
        sat_lon_use = sat_lon - 360.0
    else:
        sat_lon_use = sat_lon

    index = np.where(target_lons_use>=180.0)
    target_lons_use[index] = target_lons_use[index] - 360.0 

    #print (target_lons_use)
    #print (target_lats_use)

    #constants:
    earth_radius = 6373.0
    
    d2r = pi/180.0

    sat_lat_r = 0.0
    sat_lon_r = sat_lon_use * d2r

    target_lats_r = target_lats_use * d2r
    target_lons_r = target_lons_use * d2r

    cos_gammas = np.cos( target_lats_r ) * np.cos( target_lons_r - sat_lon_r ) 

    d = orbit_radius * ( 1.0 + (earth_radius/orbit_radius)**2.0 - 
                         2.0 * (earth_radius/orbit_radius) * cos_gammas )**0.5

    sin_gammas = np.sin( np.arccos( cos_gammas) )

    target_vzas = 90.0 - np.arccos ( sin_gammas / (d/orbit_radius)) / d2r
   
    a = np.sin(target_lats_r)
    a[abs(a)<1.0e-10] = 1.0e-10
    alpha = np.arctan ( np.tan( target_lons_r - sat_lon_r ) / a ) / d2r

    target_vaas = np.zeros(len(target_lats_use)) 

    #check target relative locations 
    lons_diff = target_lons_use - sat_lon_use
    lons_diff[lons_diff<-180.0] +=  360.0
    lons_diff[lons_diff >180.0] += -360.0

    #case 1.1 Northern Hemisphere East Station
    n_ne = np.where( (target_lats_use >= 0.0) & (lons_diff >= 0.0) )
    #case 1.2 Northern Hemisphere West Station
    n_nw = np.where( (target_lats_use >= 0.0) & (lons_diff  < 0.0) )
    #case 2.1 Southern Hemisphere East Station
    n_se = np.where( (target_lats_use  < 0.0) & (lons_diff >= 0.0) )
    #case 2.2 Southern Hemisphere West Station
    n_sw = np.where( (target_lats_use  < 0.0) & (lons_diff  < 0.0) )

    target_vaas[n_ne] = 180.0 + alpha[n_ne]
    target_vaas[n_nw] = 180.0 + alpha[n_nw]
    target_vaas[n_se] = 360.0 + alpha[n_se]
    target_vaas[n_sw] = alpha[n_sw]
    target_vaas[target_vaas>=360.0] += -360.0

    target_vzas = np.reshape(target_vzas, dims)
    target_vaas = np.reshape(target_vaas, dims)

    return {'VZA':target_vzas, 'VAA':target_vaas}
