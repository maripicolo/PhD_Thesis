import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import custom_color_palette as ccp
import main_map

# Leitura do arquivo para obtencao do LULC do cenario
vtype = xr.open_dataset('filename.nc').isel(time=0)['vtype2']

def plot_wind_temp(data):
 """
 Plot temperatura a 2 m e vento no primeiro nivel do modelo
 """
 fig, ax, trans = main_map.plot_SP_map(shapefolder=('...')) # Funcao para gerar o mapa
 clevs_temp = np.arange(22,30.02,0.2)
 ticks=[22,23,24,25,26,27,28,29,30,31,32]
 cmap = plt.get_cmap('coolwarm')
 temp_cont = ax.pcolormesh(data.lon, data.lat, data.temp2m, transform=trans, zorder=2, cmap=cmap, vmin=22, vmax=32)
 fig.colorbar(temp_cont, spacing='uniform', ticks=ticks,  extendrect=True,
                label=r"Temperatura ($^\circ$C)", orientation='horizontal', shrink=1.0,
                 aspect=30, pad=0.045)
 vtype_cont = ax.contour(
        data.lon, data.lat, vtype,levels=np.arange(17, 21, 2),
        colors='black', linewidths=1, zorder=3, transform=trans) # Plota a classe "urbano" com contorno preto
 vtype_cont = ax.contour(
        data.lon, data.lat, vtype,levels=np.arange(19, 21, 2),
        colors='darkred', linewidths=1, zorder=3, transform=trans) # Plota a classe "muito urbano" com contorno vermelho				 
 vento=ax.quiver(np.asarray(data.lon),np.asarray(data.lat), np.asarray(data.u),np.asarray(data.v), zorder=3,angles='uv', 
                 scale_units='y', scale=40.0,regrid_shape=30,transform=trans)
 plt.title(data.title_plot, weight='bold', stretch='condensed',
              size='medium', position=(0.55, 1))
 plt.savefig((data.title_figure +
                '_grade3.png'), dpi=300, bbox_inches='tight')
 plt.close()
 
def plot_wind_rv(data):
 """
 Plot razao de mistura e vento no primeiro nivel do modelo
 """
 fig, ax, trans = main_map.plot_SP_map(shapefolder=('...'))
 clevs_rv = np.arange(10,15.1,0.1)
 ticks=[10,11,12,13,14,15]
 cmap = plt.get_cmap('jet')
 rv_cont = ax.contourf(
        data.lon, data.lat,data.rv, clevs_rv, extend='both', transform=trans,zorder=2, cmap=cmap) 
 fig.colorbar(rv_cont, spacing='uniform', ticks=ticks, extendrect=True,
                label='Razão de mistura do vapor de água ($g kg^{-1}$)',orientation='horizontal', shrink=1.0,
                 aspect=30, pad=0.045)
 vtype_cont = ax.contour(
        data.lon, data.lat, vtype,levels=np.arange(17, 21, 2),
        colors='black', linewidths=1, zorder=3, transform=trans)
 vtype_cont = ax.contour(
        data.lon, data.lat, vtype,levels=np.arange(19, 21, 2),
        colors='darkred', linewidths=1, zorder=3, transform=trans)
 vento=ax.quiver(np.asarray(data.lon),np.asarray(data.lat), np.asarray(data.u),np.asarray(data.v), zorder=3,angles='uv',
                     scale_units='y', scale=40.0,regrid_shape=30,transform=trans)
 plt.title(data.title_plot, weight='bold', stretch='condensed',
              size='medium', position=(0.55, 1))
 plt.savefig((data.title_figure +
                '_grade3.png'), dpi=300, bbox_inches='tight')
 plt.close()

def plot_wind_wspd(data):
 """
 Plot velocidade do vento e vetor vento no primeiro nivel do modelo
 """
 fig, ax, trans = main_map.plot_SP_map(shapefolder=('...'))
 clevs_wspd = np.arange(0,3.1,0.1)
 ticks=[0,1,2,3]
 cmap = plt.get_cmap('jet')
 wspd_cont = ax.contourf(
        data.lon, data.lat,data.wspd, clevs_wspd, extend='max', transform=trans, zorder=2, cmap=cmap) 
 fig.colorbar(wspd_cont, spacing='uniform', ticks=ticks, extendrect=True,
                label='Velocidade do vento ($m s^{-1}$)',orientation='horizontal', shrink=1.0,
                 aspect=30, pad=0.045)
 vtype_cont = ax.contour(
        data.lon, data.lat, vtype,levels=np.arange(17, 21, 2),
        colors='black', linewidths=1, zorder=3, transform=trans)
 vtype_cont = ax.contour(
        data.lon, data.lat, vtype,levels=np.arange(19, 21, 2),
        colors='darkred', linewidths=1, zorder=3, transform=trans)
 vento=ax.quiver(np.asarray(data.lon),np.asarray(data.lat), np.asarray(data.u),np.asarray(data.v), zorder=3,angles='uv', scale_units='y', 
                scale=40.0,regrid_shape=30,transform=trans)
 plt.title(data.title_plot, weight='bold', stretch='condensed',
              size='medium', position=(0.55, 1))
 plt.savefig((data.title_figure +
                '_grade3.png'), dpi=300, bbox_inches='tight')
 plt.close()
 
def plot_h(data):
 """
 Plot calor sensivel
 """
 fig, ax, trans = main_map.plot_SP_map(shapefolder=('...'))
 clevs_h = np.arange(0,510,10)
 ticks=[0,100,200,300,400,500]
 cmap = plt.get_cmap('jet')
 cmap.set_under('white')
 h_cont = ax.contourf(
        data.lon, data.lat,data.h, clevs_h, extend='max', transform=trans, alpha=0.65,zorder=2, cmap=cmap) 
 fig.colorbar(h_cont, spacing='uniform', ticks=ticks, extendrect=True,
                label='Fluxo de calor sensível ($W m^{-2}$)',orientation='horizontal', shrink=1.0,
                 aspect=30, pad=0.045)
 vtype_cont = ax.contour(
        data.lon, data.lat, vtype,levels=np.arange(17, 21, 2),
        colors='black', linewidths=1, zorder=3, transform=trans)
 vtype_cont = ax.contour(
        data.lon, data.lat, vtype,levels=np.arange(19, 21, 2),
        colors='darkred', linewidths=1, zorder=3, transform=trans)
 plt.title(data.title_plot, weight='bold', stretch='condensed',
              size='medium', position=(0.55, 1))
 plt.savefig((data.title_figure +
                '_grade3.png'), dpi=300, bbox_inches='tight')
 plt.close()

def plot_le(data):
 """
 Plot calor latente
 """
 fig, ax, trans = main_map.plot_SP_map(shapefolder=('...'))
 clevs_le = np.arange(0,510,10)
 ticks=[0,100,200,300,400,500]
 cmap = plt.get_cmap('jet')
 cmap.set_under('white')
 le_cont = ax.contourf(
        data.lon, data.lat,data.le, clevs_le, extend='max', transform=trans, alpha=0.65,zorder=2, cmap=cmap) 
 fig.colorbar(le_cont, spacing='uniform', ticks=ticks, extendrect=True,
                label='Fluxo de calor latente ($W m^{-2}$)',orientation='horizontal', shrink=1.0,
                 aspect=30, pad=0.045)
 vtype_cont = ax.contour(
        data.lon, data.lat, vtype,levels=np.arange(17, 21, 2),
        colors='black', linewidths=1, zorder=3, transform=trans)
 vtype_cont = ax.contour(
        data.lon, data.lat, vtype,levels=np.arange(19, 21, 2),
        colors='darkred', linewidths=1, zorder=3, transform=trans)
 plt.title(data.title_plot, weight='bold', stretch='condensed',
              size='medium', position=(0.55, 1))
 plt.savefig((data.title_figure +
                '_grade3.png'), dpi=300, bbox_inches='tight')
 plt.close()
 
def plot_wind_div(data):
 """
 Plot divergencia e vento no primeiro nivel do modelo
 """
 fig, ax, trans = main_map.plot_SP_map(shapefolder=('...'))
 ticks=[-4, -3, -2, -1, 0, 1, 2, 3, 4]
 cmap = plt.get_cmap('coolwarm')
 cmap.set_over('white')
 div_cont = ax.pcolormesh(
        data.lon, data.lat, (data.div*10000), transform=trans, zorder=2, cmap=cmap,  vmin=-4, vmax=4) 
 fig.colorbar(div_cont, spacing='uniform', ticks=ticks, extendrect=True,
                label='Divergência $10^{-4}$ ($s^{-1}$)',orientation='horizontal', shrink=1.0,
                 aspect=30, pad=0.045)
 vtype_cont = ax.contour(
        data.lon, data.lat, vtype,levels=np.arange(17, 21, 2),
        colors='black', linewidths=1, zorder=3, transform=trans)
 vtype_cont = ax.contour(
        data.lon, data.lat, vtype,levels=np.arange(19, 21, 2),
        colors='darkred', linewidths=1, zorder=3, transform=trans)
 vento=ax.quiver(np.asarray(data.lon),np.asarray(data.lat), np.asarray(data.u),np.asarray(data.v), zorder=3,
                 angles='uv', scale_units='y', scale=40.0,regrid_shape=20,transform=trans)
 plt.title(data.title_plot, weight='bold', stretch='condensed',
              size='medium', position=(0.55, 1))
 plt.savefig((data.title_figure +
                '_grade3.png'), dpi=300, bbox_inches='tight')
 plt.close()

def plot_wind_refletividade(data):
 """
 Plot refletividade e vento no primeiro nivel do modelo
 """
 fig, ax, trans = main_map.plot_SP_map(shapefolder=('...'))
# defines characteristics of colors for the custom palette
 palette_1 = [['lightgray','darkgray'], ccp.range(5.0,10.0,1.0)]
 palette_2 = [['aqua','mediumblue'], ccp.range(11.0,20.0,1.0)]
 palette_3 = [['lawngreen','darkgreen'], ccp.range(21.0,35.0,0.5)]
 palette_4 = [['yellow','goldenrod'], ccp.range(36.0,50.0,0.5)]
 palette_5 = [['orangered','darkred'], ccp.range(51.0,65.0,0.5)]
# we pass the parm_color inside a list to the creates_palette module
 cmap, ticks, norm, bounds = ccp.creates_palette([palette_1, palette_2, palette_3, palette_4, palette_5])
 clevs_rain = np.arange(5,65,1)
 ticks=[5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65]
 rain_cont = ax.contourf(
        data.lon, data.lat,data.Z, clevs_rain, extend='max', transform=trans, alpha=0.65,zorder=2, cmap=cmap, norm=norm) 
 fig.colorbar(rain_cont, spacing='uniform', ticks=ticks,  extendrect=True,
              label='Refletividade (dBZ)', orientation='horizontal', shrink=1.0,
                 aspect=30, pad=0.045)
 vtype_cont = ax.contour(
        data.lon, data.lat, vtype,levels=np.arange(17, 21, 2),
        colors='black', linewidths=1, zorder=3, transform=trans)
 vtype_cont = ax.contour(
        data.lon, data.lat, vtype,levels=np.arange(19, 21, 2),
        colors='darkred', linewidths=1, zorder=3, transform=trans)
 vento=ax.quiver(np.asarray(data.lon),np.asarray(data.lat), np.asarray(data.u),np.asarray(data.v), zorder=3,angles='uv', 
                 scale_units='y', scale=40.0,regrid_shape=20,transform=trans)
 plt.title(data.title_plot, weight='bold', stretch='condensed',
              size='medium', position=(0.55, 1))
 plt.savefig((data.title_figure +
                '.png'), dpi=300, bbox_inches='tight')
 plt.close()
 
def plot_theta(data):
 """
 Plot temperatura potencial e vento no primeiro nivel do modelo
 """
 fig, ax, trans = main_map.plot_SP_map(shapefolder=('...'))
 ticks=[300,302,304, 306]
# ticks=[15,16,17,18,19,20,21,22]
 cmap = plt.get_cmap('jet')
 temp_cont = ax.pcolormesh(data.lon, data.lat, data.theta, transform=trans, alpha=0.65,zorder=2, cmap=cmap, vmin=300, vmax=306)
 fig.colorbar(temp_cont, spacing='uniform', ticks=ticks,  extendrect=True,
                label=r"Temperatura potencial ($K$)", orientation='horizontal', shrink=1.0,
                 aspect=30, pad=0.045)
 vtype_cont = ax.contour(
        data.lon, data.lat, vtype,levels=np.arange(17, 21, 2),
        colors='black', linewidths=1, zorder=3, transform=trans)
 vtype_cont = ax.contour(
        data.lon, data.lat, vtype,levels=np.arange(19, 21, 2),
        colors='darkred', linewidths=1, zorder=3, transform=trans)				 
 plt.title(data.title_plot, weight='bold', stretch='condensed',
              size='medium', position=(0.55, 1))
 plt.savefig((data.title_figure +
                '_grade3.png'), dpi=300, bbox_inches='tight')
 plt.close()
