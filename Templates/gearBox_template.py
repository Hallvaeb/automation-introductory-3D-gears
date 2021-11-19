from Shapes.Gear import Gear

#----------------------------------------------------------------------#
gear_radius_list = <RADIUS_LIST>
#----------------------------------------------------------------------#

n_gears = len(gear_radius_list)
tooth_length_please_dont_change = 2 #pretty please do not change!
prev_x = 0

for i in range(0, n_gears):
	this_gear_r = gear_radius[i]
	
	if(i == 0):
		# First gear
		x = 0
		y = 0
	else:
		x = prev_x + gear_radius[i] + gear_radius[i-1] - tooth_length_please_dont_change
		y = 0
	
	Gear(gear_radius[i], tooth_length_please_dont_change, x, y)
	prev_x = x