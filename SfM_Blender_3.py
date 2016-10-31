import bpy
import math

#<USER VARs>
pointPrefix = "Cube."
outputFilename = "deleteMe.txt"
camName = "orthoCamera"
#</USER VARs>

def RadToDeg(rad):
	deg = rad * 180.0 / math.pi
	if deg < 0:
		result = deg + 360.0
	else:
		result = deg
	return result

bpy.ops.object.select_all(action='DESELECT')

camObj = bpy.data.objects[camName]
#select and activate camera in scene...
camObj.select = True
bpy.context.scene.objects.active = camObj
#set our framecounter start
framecounter = 1
#initialize our DICT
result = {}

for obj in bpy.data.objects:
	#for all points...
	if pointPrefix in obj.name:
		#set frame...
		bpy.context.scene.frame_set(framecounter)
		#move cam to point's location...
		camObj.location = obj.location
		camObj.rotation_euler = obj.rotation_euler
		#insert location-keyframe for cam...
		bpy.ops.anim.keyframe_insert_menu(type='Location')
		bpy.ops.anim.keyframe_insert_menu(type='Rotation')
		#write cam transform into LIST...
		locrot = []
		locrot.append(camObj.location[0])
		locrot.append(camObj.location[1])
		locrot.append(camObj.location[2])
		#get the euler-rotation in radians...
		roteX = camObj.rotation_euler[0]
		roteY = camObj.rotation_euler[1]
		roteZ = camObj.rotation_euler[2]
		#convert them to degrees...
		rotX = RadToDeg(roteX)
		rotY = RadToDeg(roteY)
		rotZ = RadToDeg(roteZ)
		#...and account for Agisoft's Rotation conventions
		if rotX > 180:
			rotX = (rotX-360.0)
		if rotY > 180:
			rotY = (rotY-360.0) 
		rotZ = abs(rotZ-360.0)
		#append to locrot
		locrot.append(rotZ)
		locrot.append(rotX)
		locrot.append(rotY)
		#put LIST into DICT (key = frame)...
		result[framecounter] = locrot
		#increment framecounter...
		framecounter += 1
#This is how our DCIT should look like:   { ### : [locX, locY, locZ, rotZ, rotX, rotY] }
#</set frame, position cam, repeat>

#<write DICT to TXT file>
with open(outputFilename, "w") as text_file:
	text_file.write( "Name" + "\tEast" + "\tNorth" + "\tAltitude" + "\tYaw" + "\tPitch" + "\tRoll\n")
	
	for key, value in result.items():
		text_file.write( str(key).zfill(4) + ".jpg" + "\t")
		for item in value:
			text_file.write( str(item) + "\t")
		text_file.write("\n")
#</write DICT to TXT file>

#deselect all...
camObj.select = False
bpy.ops.object.select_all(action='DESELECT')