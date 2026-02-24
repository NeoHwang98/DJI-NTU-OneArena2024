#Initialize Values
picked_up = False
pickup_params = []
VM_List_picked_up = [13,14] #the list of valid vision markers when loaded
VM_List_no_picked_up = [11,12,13,14,15,8] #the list of valid vision markers when unloaded
distance = 2024 #set to a random large number

# Function Bank
def halt():              
    #Halts robot
    chassis_ctrl.stop()

def stop():              
    #Halts robot indefinitely, terminates program
    rm.exit()

def turn(angle,omega=60,wise=0):                       
    #Rotates. Default anticlockwise
    chassis_ctrl.set_rotate_speed(omega)
    if wise==0:
        chassis_ctrl.rotate_with_degree(rm_define.anticlockwise,angle)
    else:
        chassis_ctrl.rotate_with_degree(rm_define.clockwise,angle)

def displace(direction,displacement,speed=0.6):  
    #Move in specified direction, useful for fixed distance
    chassis_ctrl.set_trans_speed(speed)
    chassis_ctrl.move_with_distance(direction,displacement)

def move(X_speed,Y_speed,omega):       
    #Move in specified velocities, useful for curves
    chassis_ctrl.move_with_speed(X_speed,Y_speed,omega)

def wait():
    #Approach the door until specified distance away
    while True:
        distance = ir_distance_sensor_ctrl.get_distance_info(1)
        print('Approaching Door, distance=', distance)
        if distance>18:
            move(0.1,0,0)
        else:
            halt()
            break
    #Scan for large change in distance when door open, then continue
    while True:
        distance = ir_distance_sensor_ctrl.get_distance_info(1)
        print('Waiting for Door to Open, distance =',distance)
        if distance>18:
            time.sleep(1)
            break

def drop():
    global picked_up, pickup_params
    halt()
    if not picked_up:
        print('Nothing to Drop')
    else:
        turn(90)
        displace(0,0.2)
        robotic_arm_ctrl.moveto(pickup_params[0], pickup_params[1], wait_for_complete=True)
        while not gripper_ctrl.is_open():
            gripper_ctrl.open()
        print('Object Dropped')
        picked_up=False
        robotic_arm_ctrl.recenter()

def pickup():
    global distance, picked_up, pickup_params
    marker_list = []
    pid_Centralise_Marker = PIDCtrl()
    vision_ctrl.enable_detection(rm_define.vision_detection_marker)
    vision_ctrl.set_marker_detection_distance(3)
    media_ctrl.exposure_value_update(rm_define.exposure_value_large)
    ir_distance_sensor_ctrl.enable_measure(1)
    pid_Centralise_Marker.set_ctrl_params(100, 1, 0)
    #Approach Visual Marker
    while True:
        marker_list= vision_ctrl.get_marker_detection_info()
        if len(marker_list)>2:
            x_coord= marker_list[2]
            error= x_coord - 0.5 #calibrate this
            pid_Centralise_Marker.set_error(error)
            pid_output = pid_Centralise_Marker.get_output()
            distance = ir_distance_sensor_ctrl.get_distance_info(1)
            print('Pickup Marker, ID= ',marker_list[1], 'Centering...Distance =', distance)

            if distance>70:
                move(0.2, 0, pid_output)
            elif distance<70 and distance>40:
                move(0.15, 0, pid_output)
            else:
                halt()
                break
        else:
            halt()
    
    print('Centered, moving forward')
    if not picked_up:   #calibrate this
        robotic_arm_ctrl.moveto(300, -70, wait_for_complete=True)
    time.sleep(0.5)
    
    while True:
        distance=ir_distance_sensor_ctrl.get_distance_info(1)
        print('Distance from object :', distance)
        if distance>5:  #calibrate this
            move(0.1,0,0)
        else:
            halt()
            break

    print('In Position, ready for pickup')
    while (not gripper_ctrl.is_open()):
        gripper_ctrl.open()
    robotic_arm_ctrl.moveto(300, -50, wait_for_complete=True)    #calibrate this
    pickup_params = robotic_arm_ctrl.get_position()

    while (not gripper_ctrl.is_closed()):
        gripper_ctrl.close()
    robotic_arm_ctrl.recenter(wait_for_complete=True)    #calibrate this
    picked_up = True

def seek():
    global distance, picked_up, VM_List_picked_up, marker_list, VM_List, min_dist, to_drop, direction, lost_VM, pid_Centralise_Marker
    marker_list = []
    pid_Centralise_Marker= PIDCtrl()
    robotic_arm_ctrl.recenter()
    vision_ctrl.enable_detection(rm_define.vision_detection_marker)
    vision_ctrl.set_marker_detection_distance(3)
    media_ctrl.exposure_value_update(rm_define.exposure_value_large)
    ir_distance_sensor_ctrl.enable_measure(1)
    pid_Centralise_Marker.set_ctrl_params(100, 1, 0)
    direction = ''
    to_drop = False
    time.sleep(1)
    
    while True: #calibrate this
        if picked_up:
            min_dist = 13   
            VM_List=VM_List_picked_up
        else:
            min_dist=17
            VM_List=VM_List_no_picked_up

        marker_list=vision_ctrl.get_marker_detection_info()
        distance= ir_distance_sensor_ctrl.get_distance_info(1)
        print(marker_list, distance)  
        lost_VM=True
        
        corefunc(1,2)
        try:
            corefunc(6,7)
        except:
            pass
        
        #Specific Directions
        if to_drop and 0<distance<min_dist:
            print('Dropping object')
            drop()
            turn(180)
            lost_VM, to_drop= False, False

        elif direction== 'pickup':
            halt()
            pickup()
            displace(135,0.2)
            turn(178)
            wait()
            displace(0,1,speed=0.5)
            move(0.5,0,22.5)
            time.sleep(4)
            direction, to_drop= '', False


        elif direction== 'swerve' and distance<min_dist:
            print('Swerving the bend')
            turn(90,wise=1)
            displace(0,0.75)
            move(0.3,0,-59)
            time.sleep(3)
            halt()
            displace(0,0.75)
            turn(90,wise=1)
            time.sleep(0.6)
            direction, to_drop= '', False

        elif direction== 'curve_wait' and distance<min_dist*2:
            print('Curving inwards to door')
            turn(90,wise=1)
            displace(0,1.45)
            move(0.2,0,25)
            time.sleep(3.5)
            wait()
            chassis_ctrl.stop()
            direction, to_drop= '', False

        elif direction== 'right' and distance<min_dist:
            print("Rotating right")
            turn(90,wise=1)
            print("Rotation complete")
            direction, to_drop= '', False

        elif direction== 'S_Course' and distance<min_dist*2.5:
            print('Starting S-Course')
            move(0.1,0,45)
            time.sleep(3)
            displace(0,1)
            move(0.1,0,-45)
            time.sleep(3)
            VM_List_picked_up.remove(14)
            direction, to_drop= '', False

        elif direction== 'speedup_push' and distance<50: #set higher dist to account inconsistency
            chassis_ctrl.set_trans_speed(0.3)
            displace(90,2.4)
            direction, to_drop= '', False

        elif direction== 'slope':
            b_pitch= chassis_ctrl.get_attitude(rm_define.chassis_pitch)
            move(1,0,0)
            while True:
                pitch = chassis_ctrl.get_attitude(rm_define.chassis_pitch)
                print('pitch =', pitch)
                #Adjust speed base on pitch
                if pitch< b_pitch-20:
                    print('Moving downslope, pitch =', pitch)
                    move(-0.3,0,0)
                    time.sleep(1)
                    break
            stop()

        if lost_VM: #Idk why this is here, its in the original code
            print('No Visual Marker Detected, Searching...')
            if not picked_up:
                # print('Looking for Object')
                move(0.4,0,0)   
            else:
                move(0.3,0,0)

def corefunc(ID_Index,X_Coord_Index):
    global marker_list, VM_List, VM_List_picked_up, min_dist, picked_up, lost_VM, to_drop, direction, pid_Centralise_Marker
    if len(marker_list)>2 and marker_list[ID_Index] in VM_List:
        x_coord = marker_list[X_Coord_Index]

        #VM Heart
        if 8 in marker_list and picked_up:
            direction=''
        elif 8 in marker_list and not picked_up:
            direction='slope'

        #VM 1
        elif 11 in marker_list and picked_up:
            direction='right'
        elif 11 in marker_list and not picked_up:
            direction='swerve'

        #VM 2
        elif 12 in marker_list and picked_up:
            direction=''
        elif 12 in marker_list and not picked_up:
            direction='curve_wait'

        #VM 3
        elif 13 in marker_list and picked_up:
            direction=''
            to_drop=True                        #Adjust accordingly
        elif 13 in marker_list and not picked_up:
            direction='pickup'

        #VM 4
        elif 14 in marker_list and picked_up:
            direction='S_Course'
        elif 14 in marker_list and not picked_up:
            direction='S_Course'

        #VM 5
        elif 15 in marker_list and picked_up:
            direction='speedup_push'
        elif 15 in marker_list and not picked_up:
            direction='speedup_push'
        
        #VM ?
        elif 47 in marker_list and picked_up:
            direction=''
        elif 47 in marker_list and not picked_up:
            direction=''

        error= x_coord-0.5      #calibrate this
        if marker_list[ID_Index] in VM_List:
            pid_Centralise_Marker.set_error(error)
            pid_output = pid_Centralise_Marker.get_output()
            distance = ir_distance_sensor_ctrl.get_distance_info(1)
            print('Valid VM detected, ID= ', marker_list[ID_Index], 'Distance= ',distance)
        
        if distance>min_dist and not picked_up:
            speed= 0.3
        elif distance>min_dist and picked_up:
            speed= 0.2
        else:
            speed= 0
        if direction=='speedup_push': #Special Condition
            speed= 0.8

        move(speed,0,pid_output)
        print('Adjusting course and direction')
        lost_VM=False

# Active Functions
def start():
    robotic_arm_ctrl.move(0,0, wait_for_complete=True)  #Initialize Robotic Arm Neutral
    while not gripper_ctrl.is_open():
        gripper_ctrl.open()
    chassis_ctrl.set_rotate_speed(60)       #Initialize omega [0,600] degree/s
    chassis_ctrl.set_trans_speed(0.4)       #Initialize speed [0,3.5] m/s
    seek()