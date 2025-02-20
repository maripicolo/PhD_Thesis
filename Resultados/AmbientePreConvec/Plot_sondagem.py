# Programa para plotar perfis verticais de temperatura, td e vento em 5 diferentes pontos na area urbana da RMSP a partir da saida do modelo
# Utiliza o metpy para plotar e sharppy para gerar as parcelas e calcular os indices
#--------------------------------------------------------------------------------------------------------------------------------------------

from metpy.units import units
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from metpy.plots import add_timestamp, SkewT, Hodograph
import numpy as np
import xarray as xr
import sharppy.sharptab.profile as profile
import sharppy.sharptab.interp as interp
import sharppy.sharptab.winds as winds
import sharppy.sharptab.params as params
#----------------------------------------------------------------------------------------------------------------------------------------------

def plot_skewt(df, **kwargs):
    z = df['lev'].values * units.m
    T = df['tempc'].values * units.degC
    Td = df['dewptc'].values * units.degC
    u = (df['u'].values * units.meter / units.second).to(units.knots)
    v = (df['v'].values * units.meter / units.second).to(units.knots)
    p = df['press'].values * units.hPa
    
    # Cria perfil 
    prof = profile.create_profile(profile='default', pres=p, hght=z, tmpc=T, \
                                    dwpc=Td, u=u, v=v)                                     
    sfcpcl = params.parcelx(prof, flag=1,exact=True) # parcela de superficie
    mlpcl = params.parcelx(prof, flag=4,exact=True)# parcela media camada 100 hPa
    mupcl = params.parcelx(prof, flag=3,exact=True) # parcel mais instavel

    ax = plt.figure(figsize=(9,9))
    gs = gridspec.GridSpec(3, 3)
    ax.subplots_adjust(wspace=.5)
    skew = SkewT(ax, rotation=45, subplot=gs[:,:2])
    
    skew.plot(p, T, 'r')
    skew.plot(p, Td, 'g')
   # Plota as barbelas abaixo de 100 hPa
    mask = p >= 100 * units.hPa
    skew.plot_barbs(p[mask], u[mask], v[mask],flip_barb=True)
    skew.ax.set_ylim(1000, 100)
    skew.ax.set_xlim(-25, 35)
    ticks=[-20,-10,0,10,20,30]
    skew.ax.set_xticks(ticks=ticks)
    
     # Calcula a altura do LCL e LFC 
    lcl_hgt = np.round(mlpcl.lclhght,decimals=1)*units.meters
    lcl_pressure = np.round(mlpcl.lclpres,decimals=1)*units.hPa
    lfc_hgt = np.round(mlpcl.lfchght,decimals=1)*units.meters
    lfc_pressure = np.round(mlpcl.lfcpres,decimals=1)*units.hPa

    # Calcula indices termodinamicos
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
    meanq = np.round(params.mean_mixratio(prof, pbot=None, ptop=500, dp=-1, exact=False),1) * units('g/kg')

    # Calcula cisalhamento vertical do vento (1 e 6 km)
    p6km = interp.pres(prof, interp.to_msl(prof, 6000.))
    p1km = interp.pres(prof, interp.to_msl(prof, 1000.))
    u_shear01, v_shear01 = ((winds.wind_shear(prof, pbot=prof.pres[prof.sfc], ptop=p1km))*units.knots).to(units('m/s'))
    shear01 = round((np.sqrt(u_shear01**2 + v_shear01**2)), 1)
    u_shear06, v_shear06 = ((winds.wind_shear(prof, pbot=prof.pres[prof.sfc], ptop=p6km))*units.knots).to(units('m/s'))
    shear06 = round((np.sqrt(u_shear06**2 + v_shear06**2)), 1)

    # Plot do perfil da parcela como linha preta tracejada
    skew.plot(mlpcl.ptrace, mlpcl.ttrace, '--k', linewidth=2)

    
    # Plot linhas constantes de temperatura 0 e -20
    skew.ax.axvline(0, color='c', linestyle='--', linewidth=1)
    skew.ax.axvline(-20, color='c', linestyle='--', linewidth=1)

    skew.plot_dry_adiabats()
    skew.plot_moist_adiabats()
    skew.plot_mixing_lines()
    
    # Escreve na figura os indices calculados 
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
	
    # Cria hodografa 
    # Dados de vento ate 10 km
    u_hodograph = (df['u'].sel(lev=slice(0,10000)).values * units.meter / units.second).to(units.knots)
    v_hodograph = (df['v'].sel(lev=slice(0,10000)).values * units.meter / units.second).to(units.knots)
    z_hodograph = df['lev'].sel(lev=slice(0,10000)).values * units.m
    ax1 = ax.add_subplot(gs[0,-1])
    h = Hodograph(ax1, component_range=15)
    h.add_grid(increment=5)
    # Plota cada intervalo de uma cor diferente (0-1 km, 1-3km, 3-6 km, 6-9 km)
    h.plot_colormapped(u_hodograph, v_hodograph, z_hodograph, intervals = [0, 1000, 3000, 6000, 9000] * units.meters,
                 colors = ['magenta', 'red', 'yellow', 'green'], linewidth = 4)
    x_axis = ax1.xaxis
    x_axis.set_label_text("$nós$")
    x_axis.label.set_visible(True)
    y_axis = ax1.yaxis
    y_axis.set_label_text("$nós$")
    y_axis.label.set_visible(True)
	
    plt.savefig(kwargs.get('title_figure'), dpi=300, bbox_inches='tight')
    return skew
#----------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------

dataFile = 'filename.nc'

# Campo de Marte
dsSBMT = xr.open_dataset(dataFile).sel(lat=-23.50, lon=-46.63, method="nearest").isel(time=193)
date_full = dsSBMT['time'].values
date = np.datetime_as_string(date_full, unit='s').partition('T')[0]
time = np.datetime_as_string(date_full, unit='s').partition('T')[2]
time = time.replace(":", "")[:-2]
title_plot = ('Controle' + ' ' + 'Campo de Marte\n'
              + date + ' ' + time + 'UTC')
title_figure = ('SoundingSBMT' + date.replace('-', '') + time)
plot_skewt(dsSBMT, title_plot=title_plot, title_figure=title_figure, estacao='SBMT')

# Estacao IAG/USP
dsIAG = xr.open_dataset(dataFile).sel(lat=-23.65, lon=-46.62, method="nearest").isel(time=193)
date_full = dsIAG['time'].values
date = np.datetime_as_string(date_full, unit='s').partition('T')[0]
time = np.datetime_as_string(date_full, unit='s').partition('T')[2]
time = time.replace(":", "")[:-2]
title_plot = ('Controle' + ' ' + 'Água Funda/IAG\n'
              + date + ' ' + time + 'UTC')
title_figure = ('SoundingIAG' + date.replace('-', '') + time)
plot_skewt(dsIAG, title_plot=title_plot, title_figure=title_figure, estacao='IAG')

# Barueri (INMET)
dsA755 = xr.open_dataset(dataFile).sel(lat=-23.5389, lon=-46.86945, method="nearest").isel(time=193)
date_full = dsA755['time'].values
date = np.datetime_as_string(date_full, unit='s').partition('T')[0]
time = np.datetime_as_string(date_full, unit='s').partition('T')[2]
time = time.replace(":", "")[:-2]
title_plot = ('Controle' + ' ' + 'Barueri\n'
              + date + ' ' + time + 'UTC')
title_figure = ('SoundingA755' + date.replace('-', '') + time)
plot_skewt(dsA755, title_plot=title_plot, title_figure=title_figure, estacao='Barueri')

# Ponto na regiao leste de SP
dsZL = xr.open_dataset(dataFile).sel(lat=-23.455, lon=-46.31, method="nearest").isel(time=193)
date_full = dsZL['time'].values
date = np.datetime_as_string(date_full, unit='s').partition('T')[0]
time = np.datetime_as_string(date_full, unit='s').partition('T')[2]
time = time.replace(":", "")[:-2]
title_plot = ('Controle' + ' ' + 'Zona Leste\n'
              + date + ' ' + time + 'UTC')
title_figure = ('SoundingZL' + date.replace('-', '') + time)
plot_skewt(dsZL, title_plot=title_plot, title_figure=title_figure, estacao='ZL')

# Ponto no extremo norte da RMSP
dsZN = xr.open_dataset(dataFile).sel(lat=-23.44, lon=-46.71, method="nearest").isel(time=193)
date_full = dsZN['time'].values
date = np.datetime_as_string(date_full, unit='s').partition('T')[0]
time = np.datetime_as_string(date_full, unit='s').partition('T')[2]
time = time.replace(":", "")[:-2]
title_plot = ('Controle' + ' ' + 'Zona Norte\n'
              + date + ' ' + time + 'UTC')
title_figure = ('SoundingZN' + date.replace('-', '') + time)
plot_skewt(dsZN, title_plot=title_plot, title_figure=title_figure, estacao='ZN')


