# collision-wizard

This repo is a collection of tool to process and analyze vehicle collision data downloaded from the [Kentucky Collision Analysis for the Public](http://crashinformationky.org/KCAP/KYOPS/SearchWizard.aspx). 

The tools will create a heat map of collision density, a count of collisions per nearest road segment and road intersection, and create summary tables counting collisions, injuries, and fatalities by month.

The ArcGIS specific tools need a 10.1 or greater version with Spatial Analyst extension. The build table for charts tools needs Python 2.7.

Future goals are to port tools to QGIS Python.

Example of analysis: [boydx.github.io/collisions/](http://boydx.github.io/collisions/) 