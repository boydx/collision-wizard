# Import arcpy module
import arcpy

# Import environment class
from arcpy import env 
from arcpy import sa #Get Spatial Analyst Extension for Kernel Density Function
env.workspace = r'T:\L1\CollisionAnalysis_FINAL\fra.gdb'  #SET This!!!
outputspace = r'T:\L1\CollisionAnalysis_FINAL\fra.gdb' 

#Get Parameters
incsv = arcpy.GetParameterAsText(0) #input csv file with collisions
incounty = arcpy.GetParameterAsText(1) #input county for clip
inrds = arcpy.GetParameterAsText(2) #input county roads
outcollision = arcpy.GetParameterAsText(3) #output of collisions by county
outkernel = arcpy.GetParameterAsText(4) #output of kernel density 
searchdis = arcpy.GetParameterAsText(5) #seach radius for kernel density function
outintersections = arcpy.GetParameterAsText(6) #output by intersection
RdSegmentCollisions = arcpy.GetParameterAsText(7) #output by intersection
SummaryTable = arcpy.GetParameterAsText(8) #seach radius for kernel density function
templyr = "xy.lyr" #temp output for make XY layer
arcpy.CopyFeatures_management(inrds,RdSegmentCollisions)

env.extent = incounty




#import points
arcpy.MakeXYEventLayer_management(incsv,"GPS LONGITUDE DECIMAL","GPS LATITUDE DECIMAL",templyr,r'T:\L1\CollisionAnalysis\styles\wgs84.prj')

arcpy.FeatureClassToFeatureClass_conversion(templyr,outputspace,"tempcsv")

arcpy.Project_management("tempcsv","tempprj",incounty,"NAD_1983_To_WGS_1984_1")

arcpy.Clip_analysis("tempprj",incounty,outcollision)


#summary table
arcpy.Statistics_analysis(outcollision,SummaryTable,"KILLED SUM;INJURED SUM","HIT___RUN_INDICATOR")

#at intersections
arcpy.Intersect_analysis(inrds,outintersections,"","","POINT")
arcpy.Select_analysis(outcollision,"AtIntersections","INTERSECTION_ROADWAY_NAME IS NOT NULL")
arcpy.Near_analysis("AtIntersections", outintersections)
arcpy.Statistics_analysis("AtIntersections", "Table_with_summary_stats_int", "KILLED SUM;INJURED SUM;OBJECTID COUNT", "NEAR_FID")
arcpy.JoinField_management(outintersections, "OBJECTID", "Table_with_summary_stats_int", "NEAR_FID", "FREQUENCY;SUM_KILLED;SUM_INJURED;COUNT_OBJECTID")

#at segment
arcpy.Select_analysis(outcollision,"AtSegments","INTERSECTION_ROADWAY_NAME IS NULL")
arcpy.Near_analysis("AtSegments", inrds)
arcpy.Statistics_analysis("AtSegments", "Table_with_summary_stats", "KILLED SUM;INJURED SUM;OBJECTID COUNT", "NEAR_FID")

arcpy.JoinField_management(RdSegmentCollisions, "OBJECTID", "Table_with_summary_stats", "NEAR_FID", "FREQUENCY;SUM_KILLED;SUM_INJURED;COUNT_OBJECTID")

arcpy.AddField_management(RdSegmentCollisions,"CrashesPerMile","DOUBLE")
arcpy.CalculateField_management(RdSegmentCollisions,"CrashesPerMile","[FREQUENCY]/[Shape_Length]*5280")

#KD
tempkernel = arcpy.sa.KernelDensity(outcollision, "", "20", searchdis)
tempkernel.save(outkernel)

arcpy.Delete_management("tempprj")
arcpy.Delete_management("tempcsv")
arcpy.Delete_management("xy.lyr")
arcpy.Delete_management("AtIntersections")
arcpy.Delete_management("AtSegments")
arcpy.Delete_management("Table_with_summary_stats_int")
arcpy.Delete_management("Table_with_summary_stats")


