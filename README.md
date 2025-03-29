# Spatial Statistics Analysis of Glacier Loss  
**Collaborative Undergraduate Research and Inquiry 2023 Project**  

## Team  
**Faculty Advisor:** Laura Boehm Vock, PhD  
**Student Researchers:**  
- Sonam T Gurung  
- Meraf Haileslassie  
- Prasiddha Shrestha  
- Cheng Vang  

### 1st_data_orientation.Rmd:
- Co-registered file processing  
- Visualization:  
  - Pre/post coregistration plots  
  - Hillshade plots  
- Created datasets:  
  - stor_cor_df from coregistered raster  
  - stor_cor_glacier containing:  
    - Slope degrees  
    - Eastness/Northness  
    - Slope bins  
    - Curvature (plan, profile, max)  
    - Elevation  
    - Aspect  
    - Used in 3rd_z_score, 4th_variogram_rolstad

    
### 2nd_coregistered_interpolation.Rmd:
- Hypsometric interpolation method used to predict the void area
- Created 3 different polynomial regression models to predict the missing elev_diff_no_outliers
- Total volume change calculated
- Raster plot to look at the new filled in glacier
   
### 3rd_z_score.Rmd:
- Has two different datasets for the Median and NMAD models respectively
- Predicted the Median value using the Median model and the NMAD value using the piece wise model which is part of the detrending and standardization process
- Calculated the z-score using the formula (elev_diff_no_outliers - pred_med_elev_diff) / pred_mad
- Also has the Raster plot for the z-score
    

### 4th_Variogram Rolstad.Rmd:
- Uses stor_cor_na that is created from stor_cor_glacier to drop na values of z-score, takes population sample of 5000 to fit in a variogram model with z_score as response and no explanatory variables(intercept)
  
### 5th_error_prop.Rmd:
- The file contains code for calculating the final uncertainty of the overall volume change based on bins, which is the most accurate method, looking at the glacier as a whole without accounting for bins, and not accounting for spatial correlation. In this case, we used the binned uncertainty value

### 6th_kirg.Rmd:
- stor_void_zoomed created from stor_cor_glacier inorder to only look at the void area
- From stor_void_zoomed we created stor_void_na and stor.sf
- stor.sf drops na z_score values and is the data used to to model a variogram using z_score as response variable 
- stor_void_na filters na values that to help us predict
- Created predictions_z.csv after prediciton to join with stor_void_na to plot as a raster