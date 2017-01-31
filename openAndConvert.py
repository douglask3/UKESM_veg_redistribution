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

pft_names = {101: 'BET-Tr', 102: 'BDT', 103: 'BET-Te',
             201: 'NET',    202: 'NDT',
             501: 'ESH',    502: 'DSH',
               3: 'C3G',      4: 'C4G',
             301: 'C3C',    401: 'C4C',
             302: 'C3P',    402: 'C4P',
               6: 'Ur' ,      7: 'Water', 8: 'Soil',   9: 'Ice'}

plot_order = [101, 102, 103, 201, 202, 501, 502, 3, 4, 301, 401, 302, 402, 6, 7, 8, 9]
stash_contraint = iris.AttributeConstraint(STASH='m01s00i216')

###############################################
## Load mask and remove coordinate system    ##
###############################################
i = exp_dir
dir = dat_dir + i

map_points = [1, 21]

git = 'repo: ' + git_info.url + '\n' + 'rev:  ' + git_info.rev

crs_latlon = ccrs.PlateCarree()
crs_proj   = ccrs.Robinson()
cmap1 = mpl_cm.get_cmap('brewer_YlGn_09')
cmap2 = mpl_cm.get_cmap('brewer_PRGn_11')

def plot_map(fig, px, py, dat, pn, limits, cmap, title = 'yay', extend = 'max', ncolors = 8):
    norm = colours.BoundaryNorm(boundaries = limits, ncolors = ncolors)
    
    ax = fig.add_subplot(px, py, pn, projection = crs_proj)
    ax.set_extent((-180, 170, -65, 90.0), crs = crs_latlon)
    ax.coastlines(linewidth = 0.5, color = 'navy')
    ax.gridlines(crs = crs_latlon, linestyle = '--')
    
    plt.gca().coastlines()
    if (len(dat.shape) == 3 and dat.shape[0] == 1): dat = dat[0]
    
    cbi = qplt.contourf(dat, limits, cmap = cmap, extend = extend, norm = norm)
    plt.title(title)   
    #qplt.contourf(dat) 
    #plt.colorbar(cbi)
    #titlei = title + labs[i][0]  
    

def plot_fracs(cube, fig_out, sub_title, limits, cmap, ncolors, cube0 = None):
    figsize = (28, 12)
    px = 5
    py = 4
    fig = plt.figure(figsize = figsize)
    
    index  = pft_names.keys()
    points = cube[0].coord('pseudo_level').points    
    for x in range(0, len(pft_names)):
        i  = plot_order[x]
        ii = x#np.where(points == i)[0]
        browser()
        print(pft_names[i])
        if (cube0 is None):
            z = cube[0][ii]
        else:
            z = cube[0][ii] - cube0[0][ii]
        plot_map(fig, px, py, cube[0][ii], x  + 1, limits, cmap, title = pft_names[i], ncolors = ncolors)
        
    fig.suptitle(sub_title, fontsize = 16)

    fig.text(.6, .1, git)       
    plt.savefig(fig_out, bbox_inches = 'tight')

p = 0
test = False
input_files = sort(listdir(dir))
cover =np.zeros((len(pft_names),len(input_files)))
 
for input_file in input_files:
    file_in = dir + input_file
    print(file_in)
    file_out = out_dir + input_file + '.nc'
    fig1_out = fig_dir + input_file + '.pdf'
    fig2_out = fig_dir + input_file + 'diff' + '.pdf'
    cube = iris.load(file_in, stash_contraint)
   
    p = p + 1
    if (True in [p == i for i in map_points]):
        plot_fracs(cube, fig1_out, input_file, limits = [0, 0.0001, 0.001, 0.01, 0.1, 0.2, 0.5, 1], cmap = cmap1, ncolors = 8)       
        cube0 = cube
        input_file0 = input_file
                
        if test:            
            limits = [-0.1, -0.01, -0.001, -0.0001, 0.0001, 0.001, 0.01, 0.1]
            sub_title = input_file + ' - ' + input_file0
            
            plot_fracs(cube, fig2_out, sub_title, limits = limits, cmap = cmap2, ncolors = 12, cube0 = cube0)            
        
        test = True
    
    
    area =  iris.analysis.cartography.cosine_latitude_weights(cube[0][0])
    area = area / sum(area[cube[0][0].data.mask])
   
    for pft in range(0, len(pft_names)): cover[pft, p - 1] = sum(cube[0][pft].data * area)
   
#yay = iris.load('/localscratch/wllf011/rjel/ae048.astart', stash_contraint)
#iris.save(yay, 'yay.nc')


figsize = (28, 12)
px = 5
py = 4
fig = plt.figure(figsize = figsize)
index  = pft_names.keys()
points = cube[0].coord('pseudo_level').points

for x in range(0, 17):
    i  = plot_order[x]
    ii = np.where(points == i)[0]
    ax = fig.add_subplot(px, py, x + 1)
    #plt.subplots_adjust(left=1, bottom=2, right=2, top=4)
    ax.get_xaxis().get_major_formatter().set_scientific(False)
    plt.plot(range(1979, 1979 + len(input_files)),100 *cover[ii,].flatten() / 0.29)
    #
    ax.text(.5,.9,pft_names[i],
        horizontalalignment='center',
        transform=ax.transAxes)


plt.savefig('figs/TS.pdf', bbox_inches = 'tight')    

