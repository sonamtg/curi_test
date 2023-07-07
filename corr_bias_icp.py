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



# nuth and kaab and bias adjust

bias_nuth = xdem.coreg.BiasCorr() + xdem.coreg.NuthKaab()
bias_nuth.fit(reference_dem, dem_to_be_aligned, inlier_mask=inlier_mask, verbose= True)
dem_coreg = bias_nuth.apply(dem_to_be_aligned)

cor_before = dem_to_be_aligned - reference_dem
cor_after = dem_coreg - reference_dem



# compare median and nmad 


inliers_before = cor_before[inlier_mask]
med_before, nmad_before = np.median(inliers_before), xdem.spatialstats.nmad(inliers_before)

inliers_after = cor_after[inlier_mask]
med_after, nmad_after = np.median(inliers_after), xdem.spatialstats.nmad(inliers_after)

print(f"Error before: median = {med_before:.2f} - NMAD = {nmad_before:.2f} m")
print(f"Error after: median = {med_after:.2f} - NMAD = {nmad_after:.2f} m")




ax = plt.subplot(111)
cor_after.show(ax=ax, cmap="coolwarm_r", vmin=-20, vmax=20, cbar_title="Elevation change (m)")
inlier_mask.ds.plot(ax=ax, fc="none", ec="k")
plt.title("With glacier outlines")
plt.show()


ax = plt.subplot(111)
cor_before.show(ax=ax, cmap="coolwarm_r", vmin=-20, vmax=20, cbar_title="Elevation change (m)")
inlier_mask.ds.plot(ax=ax, fc="none", ec="k")
plt.title("With glacier outlines")
plt.show()




# icp bias adjust 

bias_icp = xdem.coreg.BiasCorr() + xdem.coreg.ICP()
bias_icp.fit(reference_dem, dem_to_be_aligned, inlier_mask=inlier_mask, verbose= True)
dem_icp= bias_icp.apply(dem_to_be_aligned)

icp_before = dem_to_be_aligned - reference_dem
icp_after = dem_icp - reference_dem


inliers_icp_before = icp_before[inlier_mask]
med_icp_before, nmad_icp_before = np.median(inliers_icp_before), xdem.spatialstats.nmad(inliers_icp_before)

inliers_icp_after = icp_after[inlier_mask]
med_icp_after, nmad_icp_after = np.median(inliers_icp_after), xdem.spatialstats.nmad(inliers_icp_after)

print(f"Error before: median = {med_icp_before:.2f} - NMAD = {nmad_icp_before:.2f} m")
print(f"Error after: median = {med_icp_after:.2f} - NMAD = {nmad_icp_after:.2f} m")




# plot

ax = plt.subplot(111)
icp_before.show(ax=ax, cmap="coolwarm_r", vmin=-20, vmax=20, cbar_title="Elevation change (m)")
inlier_mask.ds.plot(ax=ax, fc="none", ec="k")
plt.title("With glacier outlines")
plt.show()



ax = plt.subplot(111)
icp_after.show(ax=ax, cmap="coolwarm_r", vmin=-20, vmax=20, cbar_title="Elevation change (m)")
inlier_mask.ds.plot(ax=ax, fc="none", ec="k")
plt.title("With glacier outlines")
plt.show()



# pipeline 


pipeline = xdem.coreg.BiasCorr() + xdem.coreg.ICP() + xdem.coreg.NuthKaab()
pipeline.fit(reference_dem, dem_to_be_aligned, inlier_mask=inlier_mask, verbose= True)
dem_pipe= pipeline.apply(dem_to_be_aligned)

pipe_before = dem_to_be_aligned - reference_dem
pipe_after = dem_pipe - reference_dem


# compare median and nmad 


inliers_pipe_before = pipe_before[inlier_mask]
med_pipe_before, nmad_pipe_before = np.median(inliers_pipe_before), xdem.spatialstats.nmad(inliers_pipe_before)

inliers_pipe_after = pipe_after[inlier_mask]
med_pipe_after, nmad_pipe_after = np.median(inliers_pipe_after), xdem.spatialstats.nmad(inliers_pipe_after)

print(f"Error before: median = {med_pipe_before:.2f} - NMAD = {nmad_pipe_before:.2f} m")
print(f"Error after: median = {med_pipe_after:.2f} - NMAD = {nmad_pipe_after:.2f} m")





# plot 


ax = plt.subplot(111)
pipe_before.show(ax=ax, cmap="coolwarm_r", vmin=-20, vmax=20, cbar_title="Elevation change (m)")
inlier_mask.ds.plot(ax=ax, fc="none", ec="k")
# plt.xlim(pipe_before.bounds.left, pipe_before.bounds.right)
# plt.ylim(pipe_before.bounds.bottom, pipe_before.bounds.top)
plt.title("With glacier outlines")
plt.show()


ax = plt.subplot(111)
pipe_after.show(ax=ax, cmap="coolwarm_r", vmin=-20, vmax=20, cbar_title="Elevation change (m)")
inlier_mask.ds.plot(ax=ax, fc="none", ec="k")
# plt.xlim(pipe_before.bounds.left, pipe_before.bounds.right)
# plt.ylim(pipe_before.bounds.bottom, pipe_before.bounds.top)
plt.title("With glacier outlines")
plt.show()

# saving the coregistered data
cor_after.save("data/nk_corr.tif")
pipe_after.save("data/pipe.tif")
icp_after.save("data/icp.tif")