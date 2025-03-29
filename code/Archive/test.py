import xdem
import geoutils as gu
import matplotlib.pyplot as plt 
import numpy as np
import pandas as pd
import rasterio
import geopandas as gpd
import rasterio as rio
from rasterio.plot import show
from xdem import coreg

# outline of the glacier
outline = gu.Vector("data/Storglaciaren_Extents_2022/Storglaciaren_Extents_2022SEP.shp")

dem_2015 = xdem.DEM("data/Tarfala_Lantmatriet_2015AUG21_2M.tif")
dem_2022 = xdem.DEM("data/storglaciaren_2022_sept_uav_2m_SWEREF99_TM.tif")

print(dem_2015)
print(dem_2022)

# since the two dems are not on the same grid, we have to reproject one to another

align = dem_2022.reproject(dem_2015)
diff = align - dem_2015
print(diff) 

ax = plt.subplot(111)
diff.show(ax=ax, cmap="coolwarm_r", vmin=-20, vmax=20, cbar_title="Elevation change (m)")
outline.ds.plot(ax=ax, fc="none", ec="k")
plt.xlim(diff.bounds.left, diff.bounds.right)
plt.ylim(diff.bounds.bottom, diff.bounds.top)
plt.title("With glacier outlines")
plt.show()

diff_adj = diff - 31.28

diff_adj.show(cmap="coolwarm_r", vmin=-20, vmax=20, cbar_title="Elevation change (m)")

ax = plt.subplot(111)
diff_adj.show(ax=ax, cmap="coolwarm_r", vmin=-20, vmax=20, cbar_title="Elevation change (m)")
outline.ds.plot(ax=ax, fc="none", ec="k")
plt.xlim(diff_adj.bounds.left, diff_adj.bounds.right)
plt.ylim(diff_adj.bounds.bottom, diff_adj.bounds.top)
plt.title("With glacier outlines")
plt.show()


#lidar = rio.open("data/Tarfala_Lantmatriet_2015AUG21_2M.tif")
#ddem = rio.open("temp.tif")
#ddem_array = ddem.read(1).astype('float64')

#fig, ax = plt.subplots(1, figsize=(12, 12))
#show(ddem_array, cmap="Greys_r", ax=ax)
#plt.axis("off")
#plt.show()

#plan_curvature = xdem.terrain.planform_curvature(dem_2015)
#plan_curvature.show(cmap = "RdGy_r", vmin = -1, vmax = 1)

# Plot
#ddem.show(cmap='coolwarm_r', vmin=-20, vmax=20, cb_title="Elevation change (m)")

# Save to file
#ddem.save("temp.tif")

