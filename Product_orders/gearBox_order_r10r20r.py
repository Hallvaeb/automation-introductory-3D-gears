from Gear import Gear
import math
import NXOpen
import NXOpen.Gateway

#----------------------------------------------------------------------#
gear_radius_list = [10, 20]
project_folder_path = "C:/Users/Eier/OneDrive/Studier/TMM4270/TMM4270_A3"
photo_name = "r10r20r"
#----------------------------------------------------------------------#


n_gears = len(gear_radius_list)
tooth_length_please_dont_change = 2 # pretty please do not change!

temp_prev_x = 0
for i in range(0, n_gears):
	this_gear_r = gear_radius_list[i]
	
	if(i == 0):
		# First gear
		x = 0
		y = 0
	else:
		x = temp_prev_x + gear_radius_list[i] + gear_radius_list[i-1] - tooth_length_please_dont_change
		y = 0
	
	Gear(gear_radius_list[i], tooth_length_please_dont_change, x, y)
	temp_prev_x = x


theSession  = NXOpen.Session.GetSession()
workPart = theSession.Parts.Work
displayPart = theSession.Parts.Display

# Zoom to workpart
workPart.ModelingViews.WorkView.Orient(NXOpen.View.Canned.Trimetric, NXOpen.View.ScaleAdjustment.Fit)

# Export Image
markId1 = theSession.SetUndoMark(NXOpen.Session.MarkVisibility.Visible, "Start")
theUI = NXOpen.UI.GetUI()
imageExportBuilder1 = theUI.CreateImageExportBuilder()
imageExportBuilder1.RegionMode = False
regiontopleftpoint1 = [None] * 2 
regiontopleftpoint1[0] = 0
regiontopleftpoint1[1] = 0
imageExportBuilder1.SetRegionTopLeftPoint(regiontopleftpoint1)
imageExportBuilder1.RegionWidth = 1
imageExportBuilder1.RegionHeight = 1
imageExportBuilder1.FileFormat = NXOpen.Gateway.ImageExportBuilder.FileFormats.Png
imageExportBuilder1.FileName = project_folder_path+"/Product_images/"+photo_name+".png"
imageExportBuilder1.BackgroundOption = NXOpen.Gateway.ImageExportBuilder.BackgroundOptions.Original
imageExportBuilder1.EnhanceEdges = False
nXObject1 = imageExportBuilder1.Commit()
theSession.DeleteUndoMark(markId1, "Export Image")
imageExportBuilder1.Destroy()

# from project_folder_path.fuseki import FusekiHandler
# FusekiHandler.add_photo_name_to_gearbox(gear_radius_list, photo_name)
