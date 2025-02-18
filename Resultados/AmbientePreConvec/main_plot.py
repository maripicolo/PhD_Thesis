from read_variables import get_temp, get_rv, get_h, get_le, get_div,get_refletividade, get_theta, get_wspd
from Plot_sfc import plot_wind_temp, plot_wind_rv, plot_h, plot_le, plot_wind_div, plot_wind_refletividade, plot_theta, plot_wind_wspd
import xarray as xr

dataFile = 'Filename.nc'

#Open the dataset and print out metadeta
ds = xr.open_dataset(dataFile)
for t in range (109,264,5): # Entre 09 e 21 UTC, a cada 10 minutos
    subds_plevs = ds.isel(time=t)
    print('--- Plotting vento e temp, t = ' + str(t) + ' ---')
    plot_data = get_temp(subds_plevs)
    plot_wind_temp(plot_data)
    print('--- Plotting vento e rv, t = ' + str(t) + ' ---')
    plot_data = get_rv(subds_plevs)
    plot_wind_rv(plot_data)
    print('--- Plotting calor sensivel, t = ' + str(t) + ' ---')
    plot_data = get_h(subds_plevs)
    plot_h(plot_data)
    print('--- Plotting calor latente, t = ' + str(t) + ' ---')
    plot_data = get_le(subds_plevs)
    plot_le(plot_data)
    print('--- Plotting vento e div, t = ' + str(t) + ' ---')
    plot_data = get_div(subds_plevs)
    plot_wind_div(plot_data)
    print('--- Plotting vento e refletividade, t = ' + str(t) + ' ---')
    plot_data = get_refletividade(subds_plevs)
    plot_wind_refletividade(plot_data)
    print('--- Plotting temp potencial, t = ' + str(t) + ' ---')
    plot_data = get_theta(subds_plevs)
    plot_theta(plot_data)
    print('--- Plotting vel vento, t = ' + str(t) + ' ---')
    plot_data = get_wspd(subds_plevs)
    plot_wind_wspd(plot_data)
