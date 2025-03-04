from _libraspike_art import ffi, lib
from enum import IntEnum
from typing import Tuple
import sys
from .version import  __version__

print("LIBRASPIKE-ART STATIC "+__version__+" LOADED", file=sys.stderr)

class pbio_error(IntEnum):
    SUCCESS = lib.PBIO_SUCCESS
    FAILED = lib.PBIO_ERROR_FAILED
    INVALID_ARG = lib.PBIO_ERROR_INVALID_ARG
    IO = lib.PBIO_ERROR_IO
    BUSY = lib.PBIO_ERROR_BUSY
    NO_DEV = lib.PBIO_ERROR_NO_DEV
    NOT_IMPLEMENTED = lib.PBIO_ERROR_NOT_IMPLEMENTED
    NOT_SUPPORTED = lib.PBIO_ERROR_NOT_SUPPORTED
    AGAIN = lib.PBIO_ERROR_AGAIN
    INVALID_OP = lib.PBIO_ERROR_INVALID_OP
    TIMEDOUT = lib.PBIO_ERROR_TIMEDOUT
    CANCELED = lib.PBIO_ERROR_CANCELED

class pbio_port(IntEnum):
    ID_A = lib.PBIO_PORT_ID_A
    ID_B = lib.PBIO_PORT_ID_B
    ID_C = lib.PBIO_PORT_ID_C
    ID_D = lib.PBIO_PORT_ID_D
    ID_E = lib.PBIO_PORT_ID_E
    ID_F = lib.PBIO_PORT_ID_F

def PBIO_COLOR_ENCODE(h, s, v):
    return ((h // 30) << 3) | ((s // 51) << 2) | (v // 34)

class pbio_color(IntEnum):
    NONE = PBIO_COLOR_ENCODE(180, 0, 0)
    BLACK = PBIO_COLOR_ENCODE(0, 0, 0)
    GRAY = PBIO_COLOR_ENCODE(0, 0, 50)
    WHITE = PBIO_COLOR_ENCODE(0, 0, 100)
    RED = PBIO_COLOR_ENCODE(0, 100, 100)
    BROWN = PBIO_COLOR_ENCODE(30, 100, 50)
    ORANGE = PBIO_COLOR_ENCODE(30, 100, 100)
    YELLOW = PBIO_COLOR_ENCODE(60, 100, 100)
    GREEN = PBIO_COLOR_ENCODE(120, 100, 100)
    SPRING_GREEN = PBIO_COLOR_ENCODE(150, 100, 100)
    CYAN = PBIO_COLOR_ENCODE(180, 100, 100)
    BLUE = PBIO_COLOR_ENCODE(240, 100, 100)
    VIOLET = PBIO_COLOR_ENCODE(270, 100, 100)
    MAGENTA = PBIO_COLOR_ENCODE(300, 100, 100)

class hub_button(IntEnum):
    LEFT = lib.HUB_BUTTON_LEFT
    CENTER = lib.HUB_BUTTON_CENTER
    RIGHT = lib.HUB_BUTTON_RIGHT
    BT = lib.HUB_BUTTON_BT

class sound(IntEnum):
    MANUAL_STOP       = -1
    NOTE_C4           = 261.63
    NOTE_CS4          = 277.18
    NOTE_D4           = 293.66
    NOTE_DS4          = 311.13
    NOTE_E4           = 329.63
    NOTE_F4           = 349.23
    NOTE_FS4          = 369.99
    NOTE_G4           = 392.00
    NOTE_GS4          = 415.30
    NOTE_A4           = 440.00
    NOTE_AS4          = 466.16
    NOTE_B4           = 493.88
    NOTE_C5           = 523.25
    NOTE_CS5          = 554.37
    NOTE_D5           = 587.33
    NOTE_DS5          = 622.25
    NOTE_E5           = 659.25
    NOTE_F5           = 698.46
    NOTE_FS5          = 739.99
    NOTE_G5           = 783.99
    NOTE_GS5          = 830.61
    NOTE_A5           = 880.00
    NOTE_AS5          = 932.33
    NOTE_B5           = 987.77
    NOTE_C6           =1046.50
    NOTE_CS6          =1108.73
    NOTE_D6           =1174.66
    NOTE_DS6          =1244.51
    NOTE_E6           =1318.51
    NOTE_F6           =1396.91
    NOTE_FS6          =1479.98
    NOTE_G6           =1567.98
    NOTE_GS6          =1661.22
    NOTE_A6           =1760.00
    NOTE_AS6          =1864.66
    NOTE_B6           =1975.53

class pup_direction(IntEnum):
    CLOCKWISE = lib.PUP_DIRECTION_CLOCKWISE
    COUNTERCLOCKWISE = lib.PUP_DIRECTION_COUNTERCLOCKWISE

def raspike_open_usb_communication(device_name: str) -> ffi.CData:
    desc = lib.raspike_open_usb_communication(device_name.encode())
    return desc if desc != ffi.NULL else None

def raspike_prot_init(desc: ffi.CData) -> int:
    return lib.raspike_prot_init(desc)
def raspike_prot_receive() -> int:
    return lib.raspike_prot_receive()
def raspike_prot_shutdown() -> int:
    return lib.raspike_prot_shutdown()

def hub_system_shutdown() -> None:
    lib.hub_system_shutdown()

def hub_imu_init() -> pbio_error:
    return lib.hub_imu_init()
def hub_imu_get_acceleration() -> Tuple[float, float, float]:
    accel = ffi.new("float[3]")
    lib.hub_imu_get_acceleration(accel)
    return accel[0], accel[1], accel[2]
def hub_imu_get_angular_velocity() -> Tuple[float, float, float]:
    angv = ffi.new("float[3]")
    lib.hub_imu_get_angular_velocity(angv)
    return angv[0], angv[1], angv[2] 
def hub_imu_get_temperature() -> float:
    return lib.hub_imu_get_temperature()

def hub_display_orientation(up) -> pbio_error:
    return lib.hub_display_orientation(up)
def hub_display_off() -> pbio_error:
    return lib.hub_display_off()
def hub_display_pixel(row, column, brightness) -> pbio_error:
    return lib.hub_display_pixel(row, column, brightness)
#ToDo: pbio_error_t hub_display_image(uint8_t* image);
def hub_display_number(num: int) -> pbio_error:
    return lib.hub_display_number(num)
def hub_display_char(c: str) -> pbio_error:
    return lib.hub_display_char(c.encode())
def hub_display_text(text: str, on: int, off: int) -> pbio_error:
    return lib.hub_display_text(text.encode(), on, off)
def hub_display_text_scroll(text: str, delay: int) -> pbio_error:
    return lib.hub_display_text_scroll(text.encode(), delay)

def hub_light_on_hsv(h: int, s: int, v:int) -> pbio_error:
    hsv = ffi.new("pbio_color_hsv_t *")
    hsv.h = h
    hsv.s = s
    hsv.v = v
    return lib.hub_light_on_hsv(hsv)
def hub_light_on_color(color: pbio_color) -> pbio_error:
    return lib.hub_light_on_color(color)
def hub_light_off() -> pbio_error:
    return lib.hub_light_off()

def hub_speaker_set_volume(volume: int) -> None:
    lib.hub_speaker_set_volume(volume)
def hub_speaker_play_tone(frequency: int, duration: int) -> None:
    lib.hub_speaker_play_tone(frequency, duration)
def hub_speaker_stop() -> None:
    lib.hub_speaker_stop()

def hub_battery_get_voltage() -> int:
    return lib.hub_battery_get_voltage()
def hub_battery_get_current() -> int:
    return lib.hub_battery_get_current()

def hub_button_is_pressed(button: hub_button) -> bool:
    pressed = ffi.new("hub_button_t *")
    error = lib.hub_button_is_pressed(pressed)
    if error == pbio_error.SUCCESS:
        return pressed[0] & button
    else:
        return False

def pup_ultrasonic_sensor_get_device(port: pbio_port) -> ffi.CData:
    pdev = lib.pup_ultrasonic_sensor_get_device(port)
    return pdev if pdev != ffi.NULL else None
def pup_ultrasonic_sensor_distance(pdev: ffi.CData) -> int:
    return lib.pup_ultrasonic_sensor_distance(pdev)
def pup_ultrasonic_sensor_presence(pdev: ffi.CData) -> bool:
    return lib.pup_ultrasonic_sensor_presence(pdev)

def pup_force_sensor_get_device(port: pbio_port) -> ffi.CData:
    pdev = lib.pup_force_sensor_get_device(port)
    return pdev if pdev != ffi.NULL else None
def pup_force_sensor_force(pdev: ffi.CData) -> float:
    return lib.pup_force_sensor_force(pdev)
def pup_force_sensor_distance(pdev: ffi.CData) -> float:
    return lib.pup_force_sensor_distance(pdev)
def pup_force_sensor_pressed(pdev: ffi.CData, force: float) -> bool:
    return lib.pup_force_sensor_pressed(pdev, force)
def pup_force_sensor_touched(pdev: ffi.CData) -> bool:
    return lib.pup_force_sensor_touched(pdev)


def pup_color_sensor_get_device(port: pbio_port) -> ffi.CData:
    pdev = lib.pup_color_sensor_get_device(port)
    return pdev if pdev != ffi.NULL else None
def pup_color_sensor_rgb(pdev: ffi.CData) -> Tuple[int, int, int]:
    rgb = lib.pup_color_sensor_rgb(pdev)
    if rgb != ffi.NULL:
        return rgb.r, rgb.g, rgb.b
    else:
        return None
def pup_color_sensor_color(pdev: ffi.CData, surface: bool) -> pbio_color:
    hsv = lib.pup_color_sensor_color(pdev, surface)
    if hsv != ffi.NULL:
        return PBIO_COLOR_ENCODE(hsv.h, hsv.s, hsv.v)
    else:
        return None
def pup_color_sensor_hsv(pdev: ffi.CData, surface: bool) -> Tuple[int, int, int]:
    hsv = lib.pup_color_sensor_hsv(pdev, surface)
    if hsv != ffi.NULL:
        return hsv.h, hsv.s, hsv.v
    else:
        return None
def pup_color_sensor_reflection(pdev: ffi.CData):
    return lib.pup_color_sensor_reflection(pdev)
def pup_color_sensor_ambient(pdev: ffi.CData):
    return lib.pup_color_sensor_ambient(pdev)
def pup_color_sensor_light_set(pdev: ffi.CData, bv1: int, bv2: int, bv3: int) -> pbio_error:
    return lib.pup_color_sensor_light_set(pdev, bv1, bv2, bv3)
def pup_color_sensor_light_on(pdev: ffi.CData) -> pbio_error:
    return lib.pup_color_sensor_light_on(pdev)
def pup_color_sensor_light_off(pdev: ffi.CData) -> pbio_error:
    return lib.pup_color_sensor_light_off(pdev)
#ToDo: pup_color_hsv_t *pup_color_sensor_detectable_colors(int32_t size, pup_color_hsv_t *colors);

def pup_motor_get_device(port: pbio_port) -> ffi.CData:
    return lib.pup_motor_get_device(port)
def pup_motor_setup(motor: ffi.CData, positive_direction: pup_direction, reset_count: bool) -> pbio_error:
    return lib.pup_motor_setup(motor, positive_direction, reset_count)
def pup_motor_reset_count(motor: ffi.CData) -> pbio_error:
    return lib.pup_motor_reset_count(motor)
def pup_motor_get_count(motor: ffi.CData) -> int:
    return lib.pup_motor_get_count(motor)
def pup_motor_get_speed(motor: ffi.CData) -> int:
    return lib.pup_motor_get_speed(motor)
def pup_motor_set_speed(motor: ffi.CData, speed: int) -> pbio_error:
    return lib.pup_motor_set_speed(motor, speed)
def pup_motor_get_power(motor: ffi.CData) -> int:
    return lib.pup_motor_get_power(motor)
def pup_motor_set_power(motor: ffi.CData, power: int) -> pbio_error:
    return lib.pup_motor_set_power(motor, power)
def pup_motor_stop(motor: ffi.CData) -> pbio_error:
    return lib.pup_motor_stop(motor)
def pup_motor_brake(motor: ffi.CData) -> pbio_error:
    return lib.pup_motor_brake(motor)
def pup_motor_hold(motor: ffi.CData) -> pbio_error:
    return lib.pup_motor_hold(motor)
def pup_motor_is_stalled(motor: ffi.CData) -> bool:
    return lib.pup_motor_is_stalled(motor)
def pup_motor_set_duty_limit(motor: ffi.CData, duty_limit: int) -> int:
    return lib.pup_motor_set_duty_limit(motor, duty_limit)
def pup_motor_restore_duty_limit(motor: ffi.CData, old_value: int) -> None:
    pup_motor_restore_duty_limit(motor, old_value)
