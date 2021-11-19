from Gear import Gear

class GearTrain():

	def makeGearTrain(radius_list): 
		n_gears = len(radius_list)
		tooth_length_please_dont_change = 2 #pretty please do not change!
		prev_x = 0

		for i in range(0, n_gears):			
			
			if(i == 0):
				# First gear
				x = 0
				y = 0
			else:
				x = prev_x + radius_list[i] + radius_list[i-1] - tooth_length_please_dont_change
				y = 0
			
			Gear(radius_list[i], tooth_length_please_dont_change, x, y)
			prev_x = x