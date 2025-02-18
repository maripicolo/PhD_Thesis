import numpy as np
import matplotlib.pyplot as plt
import matplotlib
				 
def plot_wind_div(data):
 fig = plt.figure(4, figsize=(10., 8.))
 ax = plt.axes()
 ax.set_yticks([200,400,600,800,1000,1200,1400,1600,1800,2000, 2200, 2400])
 ax.set_ylim(0.0, 2400)
 ax.set_xlim(-47,-46.0)
 ax.get_yaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
 ax.get_yaxis().get_major_formatter().labelOnlyBase = False
 color_map = plt.cm.get_cmap('coolwarm')
 N = np.sqrt(data.cross_wbreeze**2+data.cross_w**2)
 u, v = data.cross_wbreeze/N, data.cross_w/N
 u *= 0.4
 v *= 3
 div_contour = ax.contourf(data.cross_lon , data.cross_lev, (data.cross_div*10000),
                        levels=np.arange(-4,4.2, 0.2),extend='both',cmap=color_map)
 div_colorbar = fig.colorbar(div_contour, label=r"Divergência $10^-4$($s^{-1}$)")
 # Vetor na figura eh uma combinacao do vento de brisa e vento vertical
 Q = ax.quiver(data.cross_lon[::4], data.cross_lev, u[::,::4], v[::,::4], color='black', pivot='mid',
            angles='uv',scale=20.0)
 qk = ax.quiverkey(Q, 0.7, 0.9, 1, r'$1 \frac{m}{s}$', labelpos='E',
                   coordinates='figure')
 w = ax.contour(data.cross_lon, data.cross_lev, data.cross_w, levels=[0.1,0.2,0.5, 1.0, 1.5], colors='gray', linewidths=2)
 rcloud_contour = ax.contour(data.cross_lon , data.cross_lev, data.cross_rcloud,
                        levels=[0.05,0.1,0.5],colors='green', linewidths=1.5)
 # Plota na parte de baixo da figura o LULC de acordo com a funcao pltcolor dentro do read_variables_cross
 vtype = ax.scatter(data.cross_lon, data.cross_vtype, c=data.cols)
 plt.title(data.title_plot, weight='bold', stretch='condensed',
              size='medium', position=(0.55, 1))
 plt.savefig(('Div' + data.title_figure +
                '_RMSP.png'), dpi=300, bbox_inches='tight')
 plt.close()
 

