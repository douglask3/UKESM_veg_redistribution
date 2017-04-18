import iris
import iris.plot      as iplt
import iris.quickplot as qplt

import matplotlib.pyplot as plt
import matplotlib.colors as colours
from   pylab             import *
import matplotlib.cm     as mpl_cm
import cartopy.crs       as ccrs

from os import listdir, getcwd, mkdir, path
from pdb import set_trace as browser

from libs import git_info

# Define paths and parameters
dat_file = 'data/qrparm.veg.frac'
fig_file = "figs/GC3.1_vegFrac.png"

pft_names = ['BL', 'NL', 'C3', 'C4', 'Shrub', 'Urban', 'Water', 'Soil', 'Ice']

cmap = mpl_cm.get_cmap('brewer_YlGn_09')
limits = [0.0, 0.01, 0.02, 0.05, 0.1, 0.2, 0.5]
###############################################
## Load mask and remove coordinate system    ##
###############################################

git = 'repo: ' + git_info.url + '\n' + 'rev:  ' + git_info.rev

crs_latlon = ccrs.PlateCarree()
crs_proj   = ccrs.Robinson()

px = 3
py = 4

def plot_map(fig, px, py, dat, pn, limits, cmap, title = 'yay', extend = 'max'):
    norm = colours.BoundaryNorm(boundaries = limits, ncolors = len(limits)+1)
    
    ax = fig.add_subplot(px, py, pn, projection = crs_proj)
    #ax.set_extent((-180, 170, -65, 90.0), crs = crs_latlon)
    ax.coastlines(linewidth = 0.5, color = 'navy')
    
    plt.gca().coastlines()
    
    cbi = iplt.contourf(dat, limits, cmap = cmap, extend = extend, norm = norm)
    plt.title(title)   
    return cbi
    

cube = iris.load_cube(dat_file)
fig = plt.figure(figsize = (12* 1.5, 6 * 1.5))

for x in range(0, cube.shape[0]):
    cbi = plot_map(fig, px, py, cube[x], x + 1, limits, cmap, title = pft_names[x])
        
fig.suptitle('GC3.1 tile frac', fontsize = 16)

colorbar_axes = plt.gcf().add_axes([0.35, 0.25, 0.5, 0.08])
colorbar = plt.colorbar(cbi, colorbar_axes, orientation='horizontal')

fig.text(.4, .1, git)       
plt.savefig(fig_file, bbox_inches = 'tight')


