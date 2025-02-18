import numpy as np
import metpy.calc as mpcalc
from metpy.interpolate import cross_section
import xarray as xr

# Leitura do arquivo para obtencao do LULC de cada cenario
data_vtype = xr.open_dataset('filename.nc').isel(time=0).metpy.parse_cf().squeeze()

class ReturnList(object):
    def __init__(self, lat, lon, cols, title_plot, title_figure, cross_lon, cross_lev, cross_w, cross_vtype,
	              cross_rcloud, cross_wbreeze, cross_div):
        self.lat = lat
        self.lon = lon
        self.cols = cols
        self.title_plot = title_plot
        self.title_figure = title_figure
        self.cross_lon = cross_lon
        self.cross_lev = cross_lev
        self.cross_w = cross_w
        self.cross_vtype = cross_vtype
        self.cross_wbreeze = cross_wbreeze
        self.cross_div = cross_div
        self.cross_rcloud = cross_rcloud
        
def pltcolor(lst):
    """
    Funcao para criar a paleta de cores para plotat o LUCL 
    Vermelho: classe "urbano"
    Vermelho escuro : classe "muito urbano"
    Azul: corpos de agua
    Verde: vegetacao
    """
    cols=[]
    for l in lst:
        if l==19:
            cols.append('red')
        elif l==21:
            cols.append('darkred')
        elif l==0:
            cols.append('blue')
        else:
            cols.append('green')
    return cols	

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

def get_crossdata(data, **kwargs):    
    lat, lon, date, time = get_main_data(data)
    title_plot = ('Controle\n'  + 
	             date + ' ' + time + ' UTC')  # pt-br
    title_figure = ('_crossplot' + date.replace('-', '') + time)

    div = mpcalc.divergence(data['u'],data['v'])
    div = div.metpy.assign_crs(grid_mapping_name='latitude_longitude', earth_radius=6371229.0)
    start = (-23.1666, -47.0)
    end = (-24.182, -46.0)
    data = data.metpy.parse_cf().squeeze()
    cross = cross_section(data, start, end)
    cross_lat = cross['lat']
    cross_lon = cross['lon']
    cross_lev = cross['lev']
    cross_vtype = cross_section(data_vtype, start, end)['vtype2']
    cols=pltcolor((data_vtype['vtype2'].sel(lat=cross_lat, lon=cross_lon, method="nearest").values.astype(int)))
    # Calculo do vento de brisa
    wbreeze = -1*(-0.7071*data['u']+0.7071*data['v'])
    cross_wbreeze = cross_section(wbreeze, start, end)
    cross_w = cross_section(data['w'], start, end)
    cross_rcloud = cross_section(data['cloud'], start, end)
    cross_div = cross_section(div, start, end)
    return ReturnList(lat=lat, lon=lon, cols=cols, title_plot=title_plot, title_figure=title_figure,
	       cross_lon=cross_lon, cross_lev=cross_lev, cross_w=cross_w, cross_vtype=cross_vtype, cross_wbreeze=cross_wbreeze,
	       cross_div=cross_div, cross_rcloud=cross_rcloud)


