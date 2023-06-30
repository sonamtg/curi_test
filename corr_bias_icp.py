import geoutils as gu
import matplotlib.pyplot as plt
import numpy as np
from xdem._typing import MArrayf, NDArrayf
import rasterio as rio
from rasterio import Affine

import xdem
from xdem import coreg, examples, misc, spatialstats


# data 
reference_dem = xdem.DEM("data/Tarfala_Lantmatriet_2015AUG21_2M.tif")
dem = xdem.DEM("data/storglaciaren_2022_sept_uav_2m_SWEREF99_TM.tif")
dem_to_be_aligned = dem.reproject(reference_dem)
outlines_2015= gu.Vector("data/Storglaciaren_Extents_2022/Storglaciaren_Extents_2022SEP.shp")
inlier_mask = ~outlines_2015.create_mask(reference_dem)


# bias corr

bias_corr = coreg.BiasCorr()
bias_corr.fit(reference_dem, dem_to_be_aligned, inlier_mask=inlier_mask)

corrected_dem = bias_corr.apply(dem_to_be_aligned)



# nuth and kaab cor 

nuth_kaab = xdem.coreg.NuthKaab()
nuth_kaab.fit(reference_dem, corrected_dem, inlier_mask=inlier_mask, verbose= True)
dem_coreg = nuth_kaab.apply(corrected_dem)

cor_before = reference_dem - corrected_dem
cor_after = reference_dem - dem_coreg



cor_after.show(cmap="coolwarm_r", vmin=-20, vmax=20, cbar_title="Elevation change (m)")
cor_before.show(cmap="coolwarm_r", vmin=-10, vmax=10, cbar_title="Elevation change (m)")



ax = plt.subplot(111)
cor_after.show(ax=ax, cmap="coolwarm_r", vmin=-20, vmax=20, cbar_title="Elevation change (m)")
outlines_2015.ds.plot(ax=ax, fc="none", ec="k")
plt.xlim(cor_after.bounds.left, cor_after.bounds.right)
plt.ylim(cor_after.bounds.bottom, cor_after.bounds.top)
plt.title("With glacier outlines")
plt.show()


ax = plt.subplot(111)
cor_after.show(ax=ax, cmap="coolwarm_r", vmin=-20, vmax=20, cbar_title="Elevation change (m)")
outlines_2015.ds.plot(ax=ax, fc="none", ec="k")
plt.xlim(cor_before.bounds.left, cor_before.bounds.right)
plt.ylim(cor_before.bounds.bottom, cor_before.bounds.top)
plt.title("With glacier outlines")
plt.show()



# icp cor 

icp = xdem.coreg.ICP()
icp.fit(reference_dem, corrected_dem, inlier_mask=inlier_mask)
dem_icp= icp.apply(corrected_dem)

icp_before = reference_dem - corrected_dem
icp_after = reference_dem - dem_icp


icp_after.show(cmap="coolwarm_r", vmin=-20, vmax=20, cbar_title="Elevation change (m)")
icp_before.show(cmap="coolwarm_r", vmin=-10, vmax=10, cbar_title="Elevation change (m)")


ax = plt.subplot(111)
icp_before.show(ax=ax, cmap="coolwarm_r", vmin=-20, vmax=20, cbar_title="Elevation change (m)")
outlines_2015.ds.plot(ax=ax, fc="none", ec="k")
plt.xlim(icp_before.bounds.left, icp_before.bounds.right)
plt.ylim(icp_before.bounds.bottom, icp_before.bounds.top)
plt.title("With glacier outlines")
plt.show()



ax = plt.subplot(111)
icp_after.show(ax=ax, cmap="coolwarm_r", vmin=-20, vmax=20, cbar_title="Elevation change (m)")
outlines_2015.ds.plot(ax=ax, fc="none", ec="k")
plt.xlim(icp_after.bounds.left, icp_after.bounds.right)
plt.ylim(icp_after.bounds.bottom, icp_after.bounds.top)
plt.title("With glacier outlines")
plt.show()



# pipeline 


pipeline = xdem.coreg.BiasCorr() + xdem.coreg.ICP() + xdem.coreg.NuthKaab()
pipeline.fit(reference_dem, corrected_dem, inlier_mask=inlier_mask)
dem_pipe= pipeline.apply(corrected_dem)

pipe_before = reference_dem - corrected_dem
pipe_after = reference_dem - dem_pipe



pipe_after.show(cmap="coolwarm_r", vmin=-20, vmax=20, cbar_title="Elevation change (m)")
pipe_before.show(cmap="coolwarm_r", vmin=-10, vmax=10, cbar_title="Elevation change (m)")



ax = plt.subplot(111)
pipe_before.show(ax=ax, cmap="coolwarm_r", vmin=-20, vmax=20, cbar_title="Elevation change (m)")
outlines_2015.ds.plot(ax=ax, fc="none", ec="k")
plt.xlim(icp_before.bounds.left, icp_before.bounds.right)
plt.ylim(icp_before.bounds.bottom, icp_before.bounds.top)
plt.title("With glacier outlines")
plt.show()


ax = plt.subplot(111)
pipe_after.show(ax=ax, cmap="coolwarm_r", vmin=-20, vmax=20, cbar_title="Elevation change (m)")
outlines_2015.ds.plot(ax=ax, fc="none", ec="k")
plt.xlim(icp_before.bounds.left, icp_before.bounds.right)
plt.ylim(icp_before.bounds.bottom, icp_before.bounds.top)
plt.title("With glacier outlines")
plt.show()

# saving the nuth and kaab dem
cor_after.save("nuth&kaab.tif")

# saving the final coregistered dem

pipe_after.save("coregistered.tif")