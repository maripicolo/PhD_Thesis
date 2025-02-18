import warnings 
warnings.filterwarnings("ignore")
import numpy as np
import matplotlib.pyplot as plt
import cartopy
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import cartopy.io.shapereader as shpreader
import cartopy.feature as cfeature
 
#def plot_SP_map(shapefolder, grid_spc=5, extent=[-48.5068, -44.5378, -25.3771, -21.7681]):
#def plot_SP_map(shapefolder, grid_spc=5, extent=[-47.5056, -45.5064, -24.4774, -22.6414]):
def plot_SP_map(shapefolder, grid_spc=5, extent=[-47.3, -45.6, -24.10, -23.15]):
 proj = cartopy.crs.PlateCarree(central_longitude=-46.5)
 trans = cartopy.crs.PlateCarree()
 fig, ax = plt.subplots(figsize=(5, 6), facecolor='w', subplot_kw=dict(projection=proj))
 ax.set_extent(extent, crs=trans)
 grid_spc_lat=0.5
 grid_spc=0.5
 shapename_SP = 'filename.shp' # Shapefile da RMSP

 resol = '10m'  # use data at this scale
 land = cartopy.feature.NaturalEarthFeature('physical', 'land', \
    scale=resol, edgecolor='k', facecolor=cfeature.COLORS['land'])
 stt_prv = cartopy.feature.NaturalEarthFeature(category='cultural', 
    name='admin_1_states_provinces_lines',
    scale='10m',facecolor='none')
 ocean = cartopy.feature.NaturalEarthFeature('physical', 'ocean', \
    scale=resol, edgecolor='none', facecolor=cfeature.COLORS['water'])

 ax.add_feature(land, linewidth=1.0 , facecolor='none', edgecolor='gray', zorder=3)
 ax.add_feature(ocean, linewidth=1.0, facecolor='none', edgecolor='gray', zorder=3)
 ax.add_feature(stt_prv, linewidth=1.0, facecolor='none', edgecolor='gray', alpha=1, zorder=3)
 ax.add_geometries(shpreader.Reader(shapename_SP).geometries(), trans,
        linewidth=1.0, facecolor='none', edgecolor='gray', zorder=3)
 gl = ax.gridlines(crs=trans, xlocs=np.arange(-180, 181, grid_spc),
                    ylocs=np.arange(-80, 90, grid_spc_lat), draw_labels=True)
		
 gl.xlabels_top = gl.ylabels_right = False
 gl.xlines = False
 gl.ylines = False
 gl.xformatter = LONGITUDE_FORMATTER
 gl.yformatter = LATITUDE_FORMATTER
 return fig, ax, trans
