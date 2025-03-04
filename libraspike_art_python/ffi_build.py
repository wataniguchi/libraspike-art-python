from cffi import FFI
import subprocess
from os import path

LIB_SOURCE = './libraspike-art/'

def clone_git():
    return subprocess.run(['git', 'clone', 'https://github.com/ETrobocon/libraspike-art.git'], text=True,
                          stdout=subprocess.PIPE).stdout.strip()

def make_lib():
    return subprocess.run(['make'], cwd=(LIB_SOURCE + 'build/obj-libraspike-art'), text=True,
                          stdout=subprocess.PIPE).stdout.strip()

ffibuilder = FFI()

if not path.isdir(LIB_SOURCE):
    clone_git()
if not path.isfile(LIB_SOURCE + 'lib/libraspike-art.a'):
    make_lib()

# include header files for libraspike-art
ffibuilder.set_source("_libraspike_art",
    """
#include "raspike_com.h"
#include "raspike_protocol_api.h"
#include "spike/pup/motor.h"
#include "spike/pup/colorsensor.h"
#include "spike/pup/forcesensor.h"
#include "spike/pup/ultrasonicsensor.h"
#include "spike/hub/system.h"
#include "spike/hub/light.h"
#include "spike/hub/imu.h"
#include "spike/hub/display.h"
#include "spike/hub/button.h"
#include "spike/hub/battery.h"
#include "spike/hub/speaker.h"
    """,
    include_dirs=[LIB_SOURCE + 'include/',
                  LIB_SOURCE + 'drivers/include/',
                  LIB_SOURCE + 'drivers/',
                  LIB_SOURCE + 'external/libpybricks/lib/pbio/include/'],
    extra_link_args=[],
    library_dirs=[LIB_SOURCE + 'lib/'],
    libraries=['raspike-art'])

# descrption of C functions to invoke from Python
ffibuilder.cdef(
    """
/* raspike_com.h */
struct _RPComDescriptor;
typedef struct _RPComDescriptor RPComDescriptor;
RPComDescriptor *raspike_open_usb_communication(const char *device_name);

/* raspike_protocol_api.h */
int raspike_prot_init(RPComDescriptor *desc);
int raspike_prot_receive(void);
int raspike_prot_shutdown(void);

/* pbio/error.h */
typedef enum {
    PBIO_SUCCESS,               /**< No error */
    PBIO_ERROR_FAILED,          /**< Unspecified error (used when no other error code fits) */
    PBIO_ERROR_INVALID_ARG,     /**< Invalid argument */
    PBIO_ERROR_IO,              /**< General I/O error */
    PBIO_ERROR_BUSY,            /**< Device or resource is busy */
    PBIO_ERROR_NO_DEV,          /**< Device is not connected */
    PBIO_ERROR_NOT_IMPLEMENTED, /**< Feature is not yet implemented */
    PBIO_ERROR_NOT_SUPPORTED,   /**< Feature is not supported on this device */
    PBIO_ERROR_AGAIN,           /**< Function should be called again later */
    PBIO_ERROR_INVALID_OP,      /**< Operation is not permitted in the current state */
    PBIO_ERROR_TIMEDOUT,        /**< The operation has timed out */
    PBIO_ERROR_CANCELED         /**< The operation was canceled */
} pbio_error_t;

/* pbio/port.h */
typedef enum {
    PBIO_PORT_ID_A = 'A', /**< I/O port labeled as "A" */
    PBIO_PORT_ID_B = 'B', /**< I/O port labeled as "B" */
    PBIO_PORT_ID_C = 'C', /**< I/O port labeled as "C" */
    PBIO_PORT_ID_D = 'D', /**< I/O port labeled as "D" */
    PBIO_PORT_ID_E = 'E', /**< I/O port labeled as "C" */
    PBIO_PORT_ID_F = 'F', /**< I/O port labeled as "F" */
} pbio_port_id_t;

/* pbio/color.h */
typedef enum {...} pbio_color_t;
typedef struct {
    /** The hue component. 0 to 359 degrees. */
    uint16_t h;
    /** The saturation component. 0 to 100 percent. */
    uint8_t s;
    /** The value component. 0 to 100 percent. */
    uint8_t v;
} pbio_color_hsv_t;

/* pbio/button.h */
typedef enum _pbio_button_flags_t {
    PBIO_BUTTON_LEFT_DOWN  = 1 << 1,
    PBIO_BUTTON_DOWN       = 1 << 2,
    PBIO_BUTTON_RIGHT_DOWN = 1 << 3,
    PBIO_BUTTON_LEFT       = 1 << 4,
    PBIO_BUTTON_CENTER     = 1 << 5,
    PBIO_BUTTON_RIGHT      = 1 << 6,
    PBIO_BUTTON_LEFT_UP    = 1 << 7,
    PBIO_BUTTON_UP         = 1 << 8,
    PBIO_BUTTON_RIGHT_UP   = 1 << 9,
} pbio_button_flags_t;

/* pbio/servo.h */
struct _pbio_servo_t;
typedef struct _pbio_servo_t pbio_servo_t;

/* spike/hub/system.h */
void hub_system_shutdown(void);

/* spike/hub/imu.h */
pbio_error_t hub_imu_init(void);
void hub_imu_get_acceleration(float accel[3]);
void hub_imu_get_angular_velocity(float angv[3]);
float hub_imu_get_temperature(void);

/* spike/hub/display.h */
pbio_error_t hub_display_orientation(uint8_t up);
pbio_error_t hub_display_off(void);
pbio_error_t hub_display_pixel(uint8_t row, uint8_t column, uint8_t brightness);
pbio_error_t hub_display_image(uint8_t* image);
pbio_error_t hub_display_number(const int8_t num);
pbio_error_t hub_display_char(const char c);
pbio_error_t hub_display_text(const char* text, uint32_t on, uint32_t off);
pbio_error_t hub_display_text_scroll(const char* text, uint32_t delay);

/* spike/hub/light.h */
pbio_error_t hub_light_on_hsv(const pbio_color_hsv_t *hsv);
pbio_error_t hub_light_on_color(pbio_color_t color);
pbio_error_t hub_light_off(void);

/* spike/hub/speaker.h */
void hub_speaker_set_volume(uint8_t volume);
void hub_speaker_play_tone(uint16_t frequency, int32_t duration);
void hub_speaker_stop(void);

/* spike/hub/battery.h */
uint16_t hub_battery_get_voltage(void);
uint16_t hub_battery_get_current(void);

/* spike/hub/button.h */
typedef enum _hub_button_t {
   HUB_BUTTON_LEFT   = PBIO_BUTTON_LEFT,
   HUB_BUTTON_CENTER = PBIO_BUTTON_CENTER,
   HUB_BUTTON_RIGHT  = PBIO_BUTTON_RIGHT,
   HUB_BUTTON_BT     = PBIO_BUTTON_RIGHT_UP,
} hub_button_t;
pbio_error_t hub_button_is_pressed(hub_button_t *pressed);

/* spike/pup_device.h */
struct _pup_device_t;
typedef struct _pup_device_t pup_device_t;

/* spike/pup/ultrasonicsensor.h */
pup_device_t *pup_ultrasonic_sensor_get_device(pbio_port_id_t port);
int32_t pup_ultrasonic_sensor_distance(pup_device_t *pdev);
bool pup_ultrasonic_sensor_presence(pup_device_t *pdev);

/* spike/pup/forcesensor.h */
pup_device_t *pup_force_sensor_get_device(pbio_port_id_t port);
float pup_force_sensor_force(pup_device_t *pdev);
float pup_force_sensor_distance(pup_device_t *pdev);
bool pup_force_sensor_pressed(pup_device_t *pdev, float force);
bool pup_force_sensor_touched(pup_device_t *pdev);

/* spike/pup/colorsensor.h */
pup_device_t *pup_color_sensor_get_device(pbio_port_id_t port);
typedef struct {
  uint16_t r, g, b;
} pup_color_rgb_t;
pup_color_rgb_t pup_color_sensor_rgb(pup_device_t *pdev);
typedef pbio_color_hsv_t pup_color_hsv_t;
pup_color_hsv_t pup_color_sensor_color(pup_device_t *pdev, bool surface);
pup_color_hsv_t pup_color_sensor_hsv(pup_device_t *pdev, bool surface);
int32_t pup_color_sensor_reflection(pup_device_t *pdev);
int32_t pup_color_sensor_ambient(pup_device_t *pdev);
pbio_error_t pup_color_sensor_light_set(pup_device_t *pdev, 
                                        int32_t bv1, int32_t bv2, int32_t bv3);
pbio_error_t pup_color_sensor_light_on(pup_device_t *pdev);
pbio_error_t pup_color_sensor_light_off(pup_device_t *pdev);
pup_color_hsv_t *pup_color_sensor_detectable_colors(int32_t size, pup_color_hsv_t *colors);

/* /spike/pup/motor.h */
typedef pbio_servo_t pup_motor_t;
typedef enum {
    PBIO_DIRECTION_CLOCKWISE,         /**< Positive means clockwise. */
    PBIO_DIRECTION_COUNTERCLOCKWISE,  /**< Positive means counterclockwise. */
} pbio_direction_t;
typedef enum {
  PUP_DIRECTION_CLOCKWISE        = PBIO_DIRECTION_CLOCKWISE,
  PUP_DIRECTION_COUNTERCLOCKWISE = PBIO_DIRECTION_COUNTERCLOCKWISE,
} pup_direction_t;
pup_motor_t *pup_motor_get_device(pbio_port_id_t port);
pbio_error_t pup_motor_setup(pup_motor_t *motor, pup_direction_t positive_direction, bool reset_count);
pbio_error_t pup_motor_reset_count(pup_motor_t *motor);
int32_t pup_motor_get_count(pup_motor_t *motor);
int32_t pup_motor_get_speed(pup_motor_t *motor);
pbio_error_t pup_motor_set_speed(pup_motor_t *motor, int speed);
int32_t pup_motor_get_power(pup_motor_t *motor);
pbio_error_t pup_motor_set_power(pup_motor_t *motor, int power);
pbio_error_t pup_motor_stop(pup_motor_t *motor);
pbio_error_t pup_motor_brake(pup_motor_t *motor);
pbio_error_t pup_motor_hold(pup_motor_t *motor);
bool pup_motor_is_stalled(pup_motor_t *motor);
int32_t pup_motor_set_duty_limit(pup_motor_t *motor, int duty_limit);
void pup_motor_restore_duty_limit(pup_motor_t *motor, int old_value);
    """)

if __name__ == "__main__":
    ffibuilder.compile(verbose=True)
