# Programa para plotar sondagem no ponto do aeroporto Campo de Marte a partir de dados do ERA5
#----------------------------------------------------------------------------------------------

from metpy.units import units
import metpy.calc as mpcalc
from metpy.plots import SkewT, Hodograph
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.ticker
import numpy as np
import xarray as xr
import sharppy
import sharppy.sharptab.profile as profile
import sharppy.sharptab.interp as interp
import sharppy.sharptab.winds as winds
import sharppy.sharptab.utils as utils
import sharppy.sharptab.params as params
import sharppy.sharptab.thermo as thermo
import sharppy.plot.skew as skew
#----------------------------------------------------------------------------------------------

def plot_skewt(df, **kwargs):
    # We will pull the data out of the example dataset into individual variables
    # and assign units.
    z = (df['z']/9.8).values * units.m
    p = df['pressure_level'].values * units.hPa
    T = (df['t'].values * units.kelvin).to(units.degC)
    q = (df['q']*1000).values * units('g/kg')
    Td = mpcalc.dewpoint_from_specific_humidity(p,T,q)
    u = (df['u'].values * units.meter / units.second).to(units.knots)
    v = (df['v'].values * units.meter / units.second).to(units.knots)
    prof = profile.create_profile(profile='default', pres=p, hght=z, tmpc=T, \
                                    dwpc=Td, u=u, v=v) 
    sfcpcl = params.parcelx(prof, flag=1,exact=True) 
    mlpcl = params.parcelx(prof, flag=4,exact=True)
    mupcl = params.parcelx(prof, flag=3,exact=True) 

    # Create a new figure. 
    ax = plt.figure(figsize=(9,9))
    # Grid for plots
    gs = gridspec.GridSpec(3, 3)
    ax.subplots_adjust(wspace=.5)
    skew = SkewT(ax, rotation=55, subplot=gs[:,:2])
   # Plot the data using normal plotting functions, in this case using
   # log scaling in Y, as dictated by the typical meteorological plot
    skew.plot(p, T, 'r')
    skew.plot(p, Td, 'g')
   # Plot barbs below 100 hPa
    mask = p >= 100 * units.hPa
    skew.plot_barbs(p, u, v,flip_barb=True)
    skew.ax.set_ylim(1000, 100)
    skew.ax.set_xlim(-25, 35)
    ticks=[-20,-10,0,10,20,30]
    skew.ax.set_xticks(ticks=ticks)
     # Calculate LCL height and plot as black dot
    lfc_hgt = mlpcl.lfchght
    if lfc_hgt > 0:
        print (lfc_hgt)
        lfc_hgt = np.round(mlpcl.lfchght, decimals=1)*units.meters
    lcl_hgt = np.round(mlpcl.lclhght,decimals=1)*units.meters
    lcl_pressure = np.round(mlpcl.lclpres,decimals=1)*units.hPa
    
    sb_cape = sfcpcl.bplus
    sb_cin = sfcpcl.bminus 
    ml_cape = mlpcl.bplus
    ml_cin = mlpcl.bminus
    mu_cape = mupcl.bplus 
    mu_cin = mupcl.bminus 
    dcape = np.round(params.dcape(prof)[0],1) * units('J/kg')
    lr_700_500 = np.round((params.lapse_rate(prof, 700, 500, pres=True))) * (units.degC / units.km)
    precipw = params.precip_water(prof,ptop=100,exact=True)
    sbcape = np.round(sb_cape, 1) * units('J/kg')
    sbcin = np.round(sb_cin, 1) * units('J/kg')
    mlcape = np.round(ml_cape, 1) * units('J/kg')
    mlcin = np.round(ml_cin, 1) * units('J/kg')
    mucape = np.round(mu_cape, 1) * units('J/kg')
    pw = round(precipw * units('in').to(units.mm),1) 
    hght0c = np.round(sfcpcl.hght0c,1) *units.meters
    hghtm10c = np.round(sfcpcl.hghtm10c,1)*units.meters
    li = np.round(mlpcl.li5) * units.degC
    meanq = np.round(params.mean_mixratio(prof, pbot=None, ptop=850, dp=-1, exact=False),1) * units('g/kg')

    p6km = interp.pres(prof, interp.to_msl(prof, 6000.))
    p1km = interp.pres(prof, interp.to_msl(prof, 1000.))
    u_shear01, v_shear01 = ((winds.wind_shear(prof, pbot=prof.pres[prof.sfc], ptop=p1km))*units.knots).to(units('m/s'))
    shear01 = round((np.sqrt(u_shear01**2 + v_shear01**2)), 1)
    u_shear06, v_shear06 = ((winds.wind_shear(prof, pbot=prof.pres[prof.sfc], ptop=p6km))*units.knots).to(units('m/s'))
    shear06 = round((np.sqrt(u_shear06**2 + v_shear06**2)), 1)

    # Calculate full parcel profile and add to plot as black line
    skew.plot(mlpcl.ptrace, mlpcl.ttrace, '--k', linewidth=2)

    
    # Slanted line at constant T -- in this case the 0
    # isotherm
    skew.ax.axvline(0, color='c', linestyle='--', linewidth=1)
    skew.ax.axvline(-20, color='c', linestyle='--', linewidth=1)

    # Add the relevant special lines
    skew.plot_dry_adiabats()
    skew.plot_moist_adiabats()
    skew.plot_mixing_lines()
    
    plt.figtext( 0.68, 0.58, 'LCL Height:')
    plt.figtext( 0.8, 0.58, f'{lcl_hgt:~P}')
    plt.figtext( 0.68, 0.56, 'LFC Height:')
    plt.figtext( 0.8, 0.56, f'{lfc_hgt:~P}')
    plt.figtext( 0.68, 0.54, 'SBCAPE:')
    plt.figtext( 0.8, 0.54, f'{sbcape:~P}')
    plt.figtext( 0.68, 0.52, 'SBCIN:')
    plt.figtext( 0.8, 0.52, f'{sbcin:~P}')
    plt.figtext( 0.68, 0.50, 'MLCAPE:')
    plt.figtext( 0.8, 0.50, f'{mlcape:~P}')
    plt.figtext( 0.68, 0.48, 'MLCIN:')
    plt.figtext( 0.8, 0.48, f'{mlcin:~P}')
    plt.figtext( 0.68, 0.46, 'MUCAPE:')
    plt.figtext( 0.8, 0.46, f'{mucape:~P}')
    plt.figtext( 0.68, 0.44, 'LI:')
    plt.figtext( 0.8, 0.44, f'{li:~P}')
    plt.figtext( 0.68, 0.42, 'DCAPE:')
    plt.figtext( 0.8, 0.42, f'{dcape:~P}')
    plt.figtext( 0.68, 0.40, 'PW:')
    plt.figtext( 0.8, 0.40, f'{pw:~P}')
    plt.figtext( 0.68, 0.38, 'Shear 0-1 km:')
    plt.figtext( 0.8, 0.38, f'{shear01:~P}')
    plt.figtext( 0.68, 0.36, 'Shear 0-6 km:')
    plt.figtext( 0.8, 0.36, f'{shear06:~P}')
    plt.figtext( 0.68, 0.34, 'Mean mixratio:')
    plt.figtext( 0.8, 0.34, f'{meanq:~P}')
   
    plt.title(kwargs.get('title_plot'), weight='bold', stretch='condensed', size=15, position=(0.55, 1))	
    
#---------------------------------------------------------------------------------------------------------------	
    # Create a hodograph
    u_hodograph = (df['u'].sel(pressure_level=slice(1000,200)).values * units.meter / units.second).to(units.knots)
    v_hodograph = (df['v'].sel(pressure_level=slice(1000,200)).values * units.meter / units.second).to(units.knots)
    z_hodograph = (df['z']/9.8).sel(pressure_level=slice(1000,200)).values * units.m
    ax1 = ax.add_subplot(gs[0,-1])
    h = Hodograph(ax1, component_range=10)
    h.add_grid(increment=5)
    h.plot_colormapped(u_hodograph, v_hodograph, z_hodograph, intervals = [0, 1000, 3000, 6000, 9000] * units.meters,
                 colors = ['magenta', 'red', 'yellow', 'green'], linewidth = 4)
    x_axis = ax1.xaxis
    x_axis.set_label_text("$nós$")
    x_axis.label.set_visible(True)
    y_axis = ax1.yaxis
    y_axis.set_label_text("$nós$")
    y_axis.label.set_visible(True)
	
    plt.savefig(kwargs.get('title_figure'), dpi=300, bbox_inches='tight')
#    plt.show()
    return skew
#--------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------

dataFile = 'Filename.nc'
# Ponto mais proximo ao aeroporto Campo de Marte
ds = xr.open_dataset(dataFile).sel(latitude=-23.50, longitude=-46.63, method="nearest").isel(valid_time=0) 
date_full = ds['valid_time'].values
date = np.datetime_as_string(date_full, unit='s').partition('T')[0]
time = np.datetime_as_string(date_full, unit='s').partition('T')[2]
time = time.replace(":", "")[:-2]
title_plot = ('ERA5 reanálise\n'
              + date + ' ' + time + 'UTC')

title_figure = ('SoundingSBMT' + date.replace('-', '') + time)
plot_skewt(ds, title_plot=title_plot, title_figure=title_figure, estacao='SBMT')



