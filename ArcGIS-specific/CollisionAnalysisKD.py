# This scripts uses ArcPy and Python 2.7 to extract create mulitple heat maps for collision points downloaded from: http://crashinformationky.org/KCAP/KYOPS/SearchWizard.aspx



# Import arcpy module
import arcpy

# Import environment class
from arcpy import env 
from arcpy import sa #Get Spatial Analyst Extension for Kernel Density Function
env.workspace = r'T:\L1\CollisionAnalysis_Example\jco.gdb'  
outputspace = r'T:\L1\CollisionAnalysis_Example\jco.gdb' 

#Get Parameters
incsv = arcpy.GetParameterAsText(0) #input csv file with collisions
incounty = arcpy.GetParameterAsText(1) #input county for clip

outcollision = arcpy.GetParameterAsText(2) #output of collisions by county
outkernel0 = arcpy.GetParameterAsText(3) #output of kernel density 
outkernel1 = arcpy.GetParameterAsText(4) #output of kernel density 
outkernel2 = arcpy.GetParameterAsText(5) #output of kernel density 
searchdis0 = arcpy.GetParameterAsText(6) #seach radius for kernel density function
searchdis1 = arcpy.GetParameterAsText(7) #seach radius for kernel density function
searchdis2 = arcpy.GetParameterAsText(8) #seach radius for kernel density function
SummaryTable = arcpy.GetParameterAsText(9) #seach radius for kernel density function
templyr = "xy.lyr" #temp output for make XY layer


env.extent = incounty #This makes sure the output extent of your raster functions match that of your county




#import points
arcpy.MakeXYEventLayer_management(incsv,"GPS LONGITUDE DECIMAL","GPS LATITUDE DECIMAL",templyr,r'T:\L1\CollisionAnalysis\styles\wgs84.prj')

arcpy.FeatureClassToFeatureClass_conversion(templyr,outputspace,"tempcsv")

arcpy.Project_management("tempcsv","tempprj",incounty,"NAD_1983_To_WGS_1984_1")

arcpy.Clip_analysis("tempprj",incounty,outcollision)


#summary table
arcpy.Statistics_analysis(outcollision,SummaryTable,"KILLED SUM;INJURED SUM","HIT___RUN_INDICATOR")



#KD
tempkernel = arcpy.sa.KernelDensity(outcollision, "", "20", searchdis0)
tempkernel.save(outkernel0)
tempkernel = arcpy.sa.KernelDensity(outcollision, "", "20", searchdis1)
tempkernel.save(outkernel1)
tempkernel = arcpy.sa.KernelDensity(outcollision, "", "20", searchdis2)
tempkernel.save(outkernel2)

arcpy.Delete_management("tempprj")
arcpy.Delete_management("tempcsv")
arcpy.Delete_management("xy.lyr")



