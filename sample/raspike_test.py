import threading
import time
import sys
import libraspike_art_python as lib
from libraspike_art_python import pbio_port, pbio_color, hub_button, sound, pup_direction, pbio_error
from simple_pid import PID

RASPIKE_COM_NAME = '/dev/USB_SPIKE'

def receiver_task():
    while True:
        lib.raspike_prot_receive()

def ultrasonicsensor_test():
    us = lib.pup_ultrasonic_sensor_get_device(pbio_port.ID_F)
    time.sleep(1)
    while True:
        print('US: Distance = %d, presence =%d' %(
	        lib.pup_ultrasonic_sensor_distance(us),
	        lib.pup_ultrasonic_sensor_presence(us)
        ))
        time.sleep(1)

def motor_test():
    mot1 = lib.pup_motor_get_device(pbio_port.ID_A)
    mot2 = lib.pup_motor_get_device(pbio_port.ID_E)
    mot3 = lib.pup_motor_get_device(pbio_port.ID_B)
    err = lib.pup_motor_setup(mot1,pup_direction.CLOCKWISE,True)
    err = lib.pup_motor_setup(mot2,pup_direction.CLOCKWISE,True)
    err = lib.pup_motor_setup(mot3,pup_direction.CLOCKWISE,True)

    for power in range(-100, 101, 10):
        lib.pup_motor_set_power(mot1,power)
        lib.pup_motor_set_power(mot2,power)
        lib.pup_motor_set_power(mot3,power)
        time.sleep(1)
    
    lib.pup_motor_stop(mot2)
    lib.pup_motor_stop(mot3)

    lib.pup_motor_set_speed(mot1,400)
    time.sleep(1)
    lib.pup_motor_stop(mot1)
    time.sleep(1)
    lib.pup_motor_set_speed(mot1,-400)
    time.sleep(1)
    lib.pup_motor_brake(mot1)
    time.sleep(1)
    lib.pup_motor_set_speed(mot1,400)  
    time.sleep(1)
    lib.pup_motor_hold(mot1)
    time.sleep(1)

    for i in range(-400, 401, 40):
        lib.pup_motor_set_speed(mot1,i)
        print('mot1:power=%d speed=%d count=%d isStall=%d' %(
            lib.pup_motor_get_power(mot1),
	        lib.pup_motor_get_speed(mot1),
	        lib.pup_motor_get_count(mot1),
            lib.pup_motor_is_stalled(mot1)
        ))
        time.sleep(1)

    lib.pup_motor_stop(mot1)

def display_test():
    lib.hub_display_number(12)
    time.sleep(3)

    lib.hub_display_char('X')
    time.sleep(2)

    #lib.hub_display_text('Ras Pike!',1000,1000)
    lib.hub_display_text_scroll('ETRobocon20th',500)

def light_test():
    lib.hub_light_on_hsv(30, 100, 100)
    time.sleep(2)
    lib.hub_light_on_color(pbio_color.GREEN)
    time.sleep(2)
    lib.hub_light_off()

def speaker_test():
    lib.hub_speaker_set_volume(50)
    lib.hub_speaker_play_tone(sound.NOTE_C5,2000)
    lib.hub_speaker_play_tone(sound.NOTE_A5,sound.MANUAL_STOP)
    time.sleep(3)
    lib.hub_speaker_stop()
    lib.hub_light_on_color(pbio_color.GREEN)
    time.sleep(3)
    #lib.hub_system_shutdown()

def colorsensor_test():
    col = lib.pup_color_sensor_get_device(pbio_port.ID_C)

    for i in range(100):
        r, g, b = lib.pup_color_sensor_rgb(col)
        print(f'[RGB]r={r} g={g} b={b}')
        h, s, v = lib.pup_color_sensor_hsv(col, True)
        print(f'[HSV]h={h} s={s} v={v}')
        time.sleep(1)

def battery_test():
    cur = lib.hub_battery_get_current()
    vol = lib.hub_battery_get_voltage()
    print(f'battery: cur={cur}, vol={vol}')

def button_test():
    while not lib.hub_button_is_pressed(hub_button.BT):
        pass
    lib.hub_speaker_set_volume(50)
    lib.hub_speaker_play_tone(sound.NOTE_A5,sound.MANUAL_STOP)
    time.sleep(1)
    lib.hub_speaker_stop()
    while not lib.hub_button_is_pressed(hub_button.CENTER):
        pass
    lib.hub_speaker_play_tone(sound.NOTE_A6,sound.MANUAL_STOP)
    time.sleep(1)
    lib.hub_speaker_stop()

def imu_test():
    if lib.hub_imu_initialize(
        [2.0, 2500.0,
        [-1.61239, -1.485107, -0.2945677], [360.4545, 356.9208, 363.781],
        [10016.18, -9657.935, 9823.967, -9957.187, 9766.231, -9970.058]]
    ) == pbio_error.SUCCESS:
    #if lib.hub_imu_initialize_by_default() == pbio_error.SUCCESS:
        time.sleep(1) # wait until IMU stablizes
        for i in range(60):
            accel = lib.hub_imu_get_acceleration()
            angv = lib.hub_imu_get_angular_velocity()
            print(f'[accel(mm/s²)] x={accel[0]} y={accel[1]} z={accel[2]} [angv(deg/s)] x={angv[0]} y={angv[1]} z={angv[2]}')
            rot = lib.hub_imu_get_orientation()
            print(f'[rot mat(deg)] m11={rot[0][0]} m12={rot[0][1]} m13={rot[0][2]} m21={rot[1][0]} m22={rot[1][1]} m23={rot[1][2]} m31={rot[2][0]} m32={rot[2][1]} m33={rot[2][2]}')
            heading = lib.hub_imu_get_heading()
            print(f'[heading] {heading}')
            time.sleep(1)

LOOP_DELAY = 0.02 # 20 ms loop
SQUARE_SIDES = 8
KP = 1.1
KI = 0.001
KD = 0.03
MAX_POWER = 100
BASE_POWER = 55
MIN_POWER = 32

def clamp(power):
    if power >= 0:
        return int(max(MIN_POWER, min(power, MAX_POWER)))
    else:
        return int(min(-MIN_POWER, max(power, -MAX_POWER)))

def drive_straight(right, left, duration_sec, target_heading):
    pid = PID(KP, KI, KD, setpoint=target_heading, sample_time=LOOP_DELAY)
    time_start = time.process_time()
    while time.process_time() - time_start < duration_sec:
        current_heading = lib.hub_imu_get_heading()
        correction = pid(current_heading)
        right_power = clamp(BASE_POWER - correction)
        left_power = clamp(BASE_POWER + correction)
        lib.pup_motor_set_power(right,right_power)
        lib.pup_motor_set_power(left,left_power)
        time.sleep(LOOP_DELAY)

def turn_to_heading(right, left, target_heading):
    pid = PID(KP, KI, KD, setpoint=target_heading, sample_time=LOOP_DELAY)
    oh_min = 1 # stat
    oh_max = 0 # stat
    oh_total = 0 # stat
    oh_count = 1 # stat
    while True:
        time_loop_start = time.process_time() # stat
        current_heading = lib.hub_imu_get_heading()
        error = target_heading - current_heading
        # normalize error to [-180, 180]
        if error > 180:
            error -= 360
        if error < -180:
            error += 360
        if abs(error) < 2.0:
            print(f'[stat] average = {oh_total/oh_count} min = {oh_min} max = {oh_max}')
            break
        power = clamp(pid(current_heading))
        lib.pup_motor_set_power(right,-power)
        lib.pup_motor_set_power(left,power)
        py_overhead = time.process_time() - time_loop_start # stat
        oh_total += py_overhead # stat
        oh_min = min(oh_min, py_overhead) # stat
        oh_max = max(oh_max, py_overhead) # stat
        oh_count += 1 # stat
        time.sleep(LOOP_DELAY)

def imu_run_test():
    if lib.hub_imu_initialize(
        [2.0, 2500.0,
        [-1.61239, -1.485107, -0.2945677], [360.4545, 356.9208, 363.781],
        [10016.18, -9657.935, 9823.967, -9957.187, 9766.231, -9970.058]]
    ) == pbio_error.SUCCESS:
    #if lib.hub_imu_initialize_by_default() == pbio_error.SUCCESS:
        right = lib.pup_motor_get_device(pbio_port.ID_A)
        left  = lib.pup_motor_get_device(pbio_port.ID_B)
        err = lib.pup_motor_setup(right,pup_direction.CLOCKWISE,True)
        err = lib.pup_motor_setup(left,pup_direction.COUNTERCLOCKWISE,True)
        time.sleep(1) # wait until IMU stablizes
        heading = lib.hub_imu_get_heading()
        print(f'[heading] initial     = {heading}')

        for i in range(SQUARE_SIDES):
            drive_straight(right, left, 3.0, heading) # 3 seconds straight
            heading = lib.hub_imu_get_heading()
            print(f'[heading] before turn = {heading}')
            heading += 90
            turn_to_heading(right, left, heading)
            heading_now = lib.hub_imu_get_heading()
            print(f'[heading] after  turn = {heading_now}')
        lib.pup_motor_stop(right)
        lib.pup_motor_stop(left)

if __name__ == "__main__":
    desc = lib.raspike_open_usb_communication(RASPIKE_COM_NAME)
    if desc is None:
        print(f"Cannot Open desc name={RASPIKE_COM_NAME}")
        sys.exit(-1)
    
    lib.raspike_prot_init(desc)

    t1 = threading.Thread(target=receiver_task,daemon=True)
    t1.start()

    #ultrasonicsensor_test()
    #display_test()
    #light_test()
    #speaker_test()
    #motor_test()
    #colorsensor_test()
    #battery_test()
    #button_test()
    imu_test()
    #imu_run_test()