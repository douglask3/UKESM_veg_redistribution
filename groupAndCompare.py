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
dat_files  = ['data/qrparm.veg.frac',
              '../JULES_UKESM_albedo/data/JULES-ES.1p6.vn4.7.S3.Annual.landCoverFrac.nc']       
names      = ['GC3.1', 'JULES offline']
   
fig_file   = "figs/tileFracs"

tile_9names  = ['BL', 'NL', 'C3', 'C4', 'Shrub', 'Urban', 'Water', 'Soil', 'Ice']
tile_17names = ['BD','TBE','tBE','NLD','NLE','C3G','C3C','C3P','C4G','C4C','C4P','SHD','SHE','Urban','Lake','Bare Soil','Ice']
pft_17_2_9   = [ 1  , 1   , 1   , 2   , 2  , 3    , 3   , 3   , 4   , 4   , 4   , 5   , 5   , 6     , 7    , 8         , 9   ] 

cmap    = plt.get_cmap('brewer_YlGn_09')
dcmap   = plt.get_cmap('brewer_PiYG_11')
limits  = [0.0, 0.01, 0.02, 0.05, 0.1, 0.2, 0.5]
dlimits = [-1, -0.5, -0.2, -0.1, -0.01, 0.01, 0.1, 0.2, 0.5, 1]
###############################################
## Load mask and remove coordinate system    ##
###############################################

git = 'repo: ' + git_info.url + '\n' + 'rev:  ' + git_info.rev

crs_latlon = ccrs.PlateCarree()
crs_proj   = ccrs.Robinson()

pxs = [3, 5]
pys = [4, 4]

def plot_map(fig, px, py, dat, pn, limits, cmap = mpl_cm.get_cmap('brewer_YlGn_09'),
             title = 'yay', extend = 'max'):
    
    ncolors = len(limits) + (2 if extend == 'both' else 1)
    #if extend == 'max' : ncolors += 1
    #if extend == 'min' : ncolors += 1
    #browser()
    norm = colours.BoundaryNorm(boundaries = limits, ncolors = ncolors)
    
    ax = fig.add_subplot(px, py, pn, projection = crs_proj)
    #ax.set_extent((-180, 170, -65, 90.0), crs = crs_latlon)
    ax.coastlines(linewidth = 0.5, color = 'navy')
    
    plt.gca().coastlines()
    
    cbi = iplt.contourf(dat, limits, cmap = cmap, extend = extend, norm = norm)
    plt.title(title)   
    return cbi


def plot_tiles(name, cube, *args, **kw):
    if cube.shape[0] == 9:
        px = pxs[0]
        py = pys[0]
        tile_names = tile_9names
    else:
        px = pxs[1]
        py = pys[1]
        tile_names = tile_17names

    fig = plt.figure(figsize = (12* 1.5, 6 * 1.5))

    for x in range(0, cube.shape[0]):
        #if x == 16: browser()
        cbi = plot_map(fig, px, py, cube[x], x + 1, title = tile_names[x], 
                       *args, **kw)
        
    fig.suptitle(name, fontsize = 16)

    colorbar_axes = plt.gcf().add_axes([0.35, 0.25, 0.5, 0.08])
    colorbar = plt.colorbar(cbi, colorbar_axes, orientation='horizontal')
    fig_file = "figs/tileFracs" + name + '.png'
    fig.text(.4, .1, git)       
    plt.savefig(fig_file, bbox_inches = 'tight')


cubes = iris.load(dat_files)
gc3p1 = cubes[0]
jules = cubes[2] 
jules_end = jules[140:150].collapsed('time', iris.analysis.MEAN)

jules_groups = jules_end[0:9].copy()
jules_groups.data[:]= 0.0

for i in range(1,10):
    index = np.where(np.array(pft_17_2_9) == i)
    for j in index[0]:
        jules_groups.data[i - 1] += jules_end.data[j]
    #return jules_groups

#jules_groups = [makeGroup(i) for i in range(1,10)]

plot_tiles('GC3.1', gc3p1, limits = limits, cmap = cmap)
plot_tiles('JULES_offline', jules_end, limits = limits, cmap = cmap)
plot_tiles('JULES_offline_grouped', jules_groups, limits = limits, cmap = cmap)

diff = gc3p1.copy()

maxLat = jules_groups.coord('latitude').points[-1] + 0.01
minLat = jules_groups.coord('latitude').points[ 0] - 0.01
diff = diff.extract(iris.Constraint(latitude=lambda cell: cell < maxLat))
diff = diff.extract(iris.Constraint(latitude=lambda cell: cell > minLat))
diff.data -= jules_groups.data
diff.data = -diff.data

plot_tiles('Jules offline - GC3.1', diff, limits = dlimits, cmap = dcmap, extend = 'neither')
browser()
