from read_variables_cross import get_crossdata
from Plot_crosssection import plot_wind_div
import xarray as xr

#Open the dataset 
ds = xr.open_dataset('filename.nc')

#for t in range(33, 48):
#for t in range(27, 36):

# Plot cross sections
for t in range (109,254,2): # Entre 14 e 21 UTC, a cada 10 minutos
    subds_plevs = ds.isel(time=t)
    print('--- Plotting vento hor e div, t = ' + str(t) + ' ---')
    plot_data = get_crossdata(subds_plevs)
    plot_wind_div(plot_data)


