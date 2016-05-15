# Import arcpy module
import arcpy

# Import environment class
from arcpy import env
env.workspace = r'T:\L1\StateData.gdb'

#Create paramater input function
inexpression = arcpy.GetParameterAsText(0)
cntyname = arcpy.GetParameterAsText(1)
cntyrds = arcpy.GetParameterAsText(2)

expression = "NAME = '" + inexpression.upper() + "'"

arcpy.Select_analysis("KentuckyCounty",cntyname,expression)
arcpy.Clip_analysis("KentuckyRoads",cntyname,cntyrds)

