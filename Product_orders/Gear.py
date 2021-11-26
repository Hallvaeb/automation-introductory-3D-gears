from Shapes.Cylinder import Cylinder
from Shapes.Block_2 import Block_2
import NXOpen
import math

def Gear (gear_radius, tooth_length, x, y):
	teeth = math.floor(gear_radius / 0.8)
	angle = 2*math.pi / teeth
	cylinder_radius = gear_radius-tooth_length
	cylinder_height = cylinder_radius/5
	gear = Cylinder(x,y,0, cylinder_radius * 2, cylinder_height,  [0,0,1])
	for i in range(0, teeth):
		tooth = Block_2(x + (cylinder_radius-0.1*tooth_length)*math.cos(i*angle),
            y + (cylinder_radius-0.1*tooth_length)*math.sin(i*angle),
			0,
			tooth_length,
			tooth_length,
			cylinder_height,
			NXOpen.Vector3d(math.cos(i*angle), math.sin(i*angle), 0.0),
			NXOpen.Vector3d(math.cos(i*angle+math.pi/2), math.sin(i*angle+math.pi/2),0.0))
		gear.unite(tooth)
	hole_in_gear = Cylinder(x, y, 0, cylinder_radius/15, cylinder_height,[0,0,1])
	gear.subtract(hole_in_gear)

	return gear