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
dat_dir = "data/"
exp_dir = "af398/"
out_dir = "outputs/"
fig_dir = "figs/"

pft_names = [['C3G'],['C4G'],['??'],['Lake'],['Soil'],['Ice'],['BDT'],['BET-Tr'],['BET-Te'],['NET'],['NDT'],['C3C'],['C3P'],['C4C'],[' C4P'],['ESH'],['DSH']]
stash_contraint = iris.AttributeConstraint(STASH='m01s00i216')

###############################################
## Load mask and remove coordinate system    ##
###############################################
i = exp_dir
dir = dat_dir + i

map_points = [1, 2]

git = 'repo: ' + git_info.url + '\n' + 'rev:  ' + git_info.rev

crs_latlon = ccrs.PlateCarree()
crs_proj   = ccrs.Robinson()
cmap1 = mpl_cm.get_cmap('brewer_YlGn_09')
cmap2 = mpl_cm.get_cmap('brewer_PRGn_11')

def plot_map(fig, px, py, dat, pn, limits = [0, 0.0001, 0.001, 0.01, 0.1, 0.2, 0.5, 1], cmap = cmap1, title = 'yay', extend = 'max'):
    norm = colours.BoundaryNorm(boundaries = limits, ncolors = 8)

    ax = fig.add_subplot(px, py, pn, projection = crs_proj)
    ax.set_extent((-180, 170, -65, 90.0), crs = crs_latlon)
    ax.coastlines(linewidth = 0.5, color = 'navy')
    ax.gridlines(crs = crs_latlon, linestyle = '--')
    
    plt.gca().coastlines()
    cbi = qplt.contourf(dat, limits, cmap = cmap, extend = extend, norm = norm) 
    #qplt.contourf(dat) 
    #plt.colorbar(cbi)
    #titlei = title + labs[i][0]  
    plt.title(title)

def plot_fracs(cube, fig_out, sub_title, *args):
    figsize = (28, 16)
    px = 5
    py = 4
    fig = plt.figure(figsize = figsize)
    browser()
    for x in range(0, 17): plot_map(fig, px, py, cube[0][x], x  + 1, title = pft_names[x], *args)
        
    fig.suptitle(sub_title, fontsize = 16)

    fig.text(.6, .1, git)       
    plt.savefig(fig1_out, bbox_inches = 'tight')

p = 0
test = False
input_files = ['af398a.da19781201_00', 'af398a.da19931201_00']
for input_file in input_files:
    file_in = dir + input_file
    file_out = out_dir + input_file + '.nc'
    fig1_out = fig_dir + input_file + '.pdf'
    fig2_out = fig_dir + input_file + 'diff' + '.pdf'

    cube = iris.load(file_in, stash_contraint)
   
    p = p + 1
    if (True in [p == i for i in map_points]):
        plot_fracs(cube, fig1_out, input_file)       
        cube0 = cube
        input_file0 = input_file
                
        if test:            
            limits = [-0.1, -0.01, -0.001, -0.0001, 0.0001, 0.001, 0.01, 0.1]
            sub_title = input_file + ' - ' + input_file0
            plot_fracs(cube, fig2_out, sub_title, limits = limits, cmap = cmap2)            
        
        test = True
       
#yay = iris.load('/localscratch/wllf011/rjel/ae048.astart', stash_contraint)
#iris.save(yay, 'yay.nc')
