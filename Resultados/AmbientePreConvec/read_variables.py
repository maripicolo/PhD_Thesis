import numpy as np
import scipy.ndimage as ndimage
import metpy.calc as mpcalc

import xarray as xr

class ReturnList(object):
    def __init__(self, lat, lon, title_plot, title_figure, temp2m, u, v, rv, wspd, h, le, 
	            div, Z, theta, vb):
        self.lat = lat
        self.lon = lon
        self.title_plot = title_plot
        self.title_figure = title_figure
        self.temp2m = temp2m
        self.u = u
        self.v = v
        self.rv = rv
        self.wspd = wspd
        self.h = h
        self.le = le
        self.div = div
        self.Z = Z
        self.theta = theta
		
def get_main_data(data):
    """
    """

    lat = data['lat']
    lon = data['lon']  # - 180
    date_full = data['time'].values
    date = np.datetime_as_string(date_full, unit='s').partition('T')[0]
    time = np.datetime_as_string(date_full, unit='s').partition('T')[2]
    time = time.replace(":", "")[:-2]

    return lat, lon, date, time
    

def get_temp(data_sfc, **kwargs):
    """
    """

    lat, lon, date, time = get_main_data(data_sfc)
    title_plot = (date + ' ' + time + ' UTC')  # pt-br
    title_figure = ('_vento_temp_sfc' + date.replace('-', '') + time)

    u = data_sfc['u'].sel(lev=23.9)
    v = data_sfc['v'].sel(lev=23.9)
    temp2m = data_sfc['tempc2m']
    return ReturnList(lat=lat, lon=lon, title_plot=title_plot, title_figure=title_figure, temp2m=temp2m,
	 u=u, v=v, rv=None, wspd=None, h=None, le=None, div=None,Z=None, theta=None)

def get_rv(data_sfc, **kwargs):
    """
    """

    lat, lon, date, time = get_main_data(data_sfc)
    title_plot = (date + ' ' + time + ' UTC')  # pt-br
    title_figure = ('_vento_rv_sfc' + date.replace('-', '') + time)

    u = data_sfc['u'].sel(lev=23.9)
    v = data_sfc['v'].sel(lev=23.9)
    rv = data_sfc['rv'].sel(lev=23.9)
    return ReturnList(lat=lat, lon=lon, title_plot=title_plot, title_figure=title_figure, temp2m=None,
	 u=u, v=v, rv=rv, wspd=None, h=None, le=None, div=None, Z=None, theta=None)

def get_wspd(data_sfc, **kwargs):
    """
    """

    lat, lon, date, time = get_main_data(data_sfc)
    title_plot = (date + ' ' + time + ' UTC')  # pt-br
    title_figure = ('_vento_wspd_sfc' + date.replace('-', '') + time)

    u = data_sfc['u'].sel(lev=23.9)
    v = data_sfc['v'].sel(lev=23.9)
    wspd = np.sqrt(u**2 + v**2)
    return ReturnList(lat=lat, lon=lon, title_plot=title_plot, title_figure=title_figure, temp2m=None,
	 u=u, v=v, rv=None, wspd=wspd, h=None, le=None, div=None, Z=None, theta=None)
	 
def get_h(data_sfc, **kwargs):
    """
    """

    lat, lon, date, time = get_main_data(data_sfc)
    title_plot = (date + ' ' + time + ' UTC')  # pt-br
    title_figure = ('_Calor_sensivel' + date.replace('-', '') + time)

    u = data_sfc['u'].sel(lev=23.9)
    v = data_sfc['v'].sel(lev=23.9)
    h = data_sfc['h']
    return ReturnList(lat=lat, lon=lon, title_plot=title_plot, title_figure=title_figure, temp2m=None,
	 u=u, v=v, rv=None, wspd=None, h=h, le=None, div=None, Z=None,theta=None)

def get_le(data_sfc, **kwargs):
    """
    """

    lat, lon, date, time = get_main_data(data_sfc)
    title_plot = (date + ' ' + time + ' UTC')  # pt-br
    title_figure = ('_Calor_latente' + date.replace('-', '') + time)

    u = data_sfc['u'].sel(lev=23.9)
    v = data_sfc['v'].sel(lev=23.9)
    le = data_sfc['le']
    return ReturnList(lat=lat, lon=lon, title_plot=title_plot, title_figure=title_figure, temp2m=None,
	 u=u, v=v, rv=None, wspd=None, h=None, le=le, div=None, Z=None,theta=None)

def get_div(data_sfc, **kwargs):
    """
    """

    lat, lon, date, time = get_main_data(data_sfc)
    title_plot = (date + ' ' + time + ' UTC')  # pt-br
    title_figure = ('_vento_div_sfc' + date.replace('-', '') + time)

    u = data_sfc['u'].sel(lev=23.9)
    v = data_sfc['v'].sel(lev=23.9)
    dx, dy = mpcalc.lat_lon_grid_deltas(lon, lat)	
    div = mpcalc.divergence(u,v, dx=dx, dy=dy)
    return ReturnList(lat=lat, lon=lon, title_plot=title_plot, title_figure=title_figure, temp2m=None,
	 u=u, v=v, rv=None, wspd=None, h=None, le=None, div=div, Z=None, theta=None)


def get_refletividade(data_sfc, **kwargs):
    """
    """

    lat, lon, date, time = get_main_data(data_sfc)
    title_plot = (date + ' ' + time + ' UTC')  # pt-br
    title_figure = ('_vento_refletividade' + date.replace('-', '') + time)

    u = data_sfc['u'].sel(lev=23.9)
    v = data_sfc['v'].sel(lev=23.9)
    Z = 10*np.log10(200*(data_sfc['pcprate']**1.6))    
    return ReturnList(lat=lat, lon=lon, title_plot=title_plot, title_figure=title_figure, temp2m=None,
	 u=u, v=v, rv=None,wspd=None, h=None, le=None, div=None, Z=Z, theta=None)
	 	 
def get_theta(data_sfc, **kwargs):
    """
    """

    lat, lon, date, time = get_main_data(data_sfc)
    title_plot = (date + ' ' + time + ' UTC')  # pt-br
    title_figure = ('_Temp_potencial' + date.replace('-', '') + time)

    u = data_sfc['u'].sel(lev=23.9)
    v = data_sfc['v'].sel(lev=23.9)
    theta = data_sfc['theta'].sel(lev=23.9)   
    return ReturnList(lat=lat, lon=lon, title_plot=title_plot, title_figure=title_figure, temp2m=None,
	 u=u, v=v, rv=None, wspd=None, h=None, le=None, div=None, Z=None, theta=theta)

	 
