"""A Python program that demonstrates how to use the Arduino Cloud service.

Description
-----------

A Python program that demonstrates how to use the Arduino Cloud service.

The program configures and connects the cloud variables representing the
connected LED and button to the service over WiFi.

The LED and button can be controlled and monitored from a dashboard.

The following cloud variables (linked local variables) are used within the
program.

- ButtonState (button_state)
- DebugMessage (debug_message)
- LEDState (led_state)

Circuit
-------

- An LED is connected to BCM pin 21, physical pin 40.
- A (normally open) momentary push button is connected to BCM pin 5,
  physical pin 29.

Libraries/Modules
-----------------

- *logging* Standard Library
    - https://docs.python.org/3/library/logging.html
    - Used by the *Arduino IoT Cloud Python Client* library to print information
      to the screen.
- *Arduino IoT Cloud Python Client* Library
    - https://github.com/arduino/arduino-iot-cloud-py
    - Provides support for the Arduino Cloud service.
- *GPIO Zero* Library
    - https://gpiozero.readthedocs.io
    - Provides GPIO and connected devices support on the Raspberry Pi.
- *secrets* Local Module
    - Contains the secrets used for accessing the Arduino Cloud service.

Notes
-----

- The separate *secrets.py* module contains the secrets used for accessing the
  Arduino Cloud service.  Replace the secret placeholders (*your_device_id* and
  *your_secret_key*) within that file with the appropriate values for your setup
  before running this program.
- Debug messages are printed to the screen and sent to the Arduino Cloud
  dashboard when the *DEBUG* flag is enabled.
- Comments are Sphinx (reStructuredText) compatible.

TODO
----

- None.

Author(s)
---------

- Created by John Woolsey on 11/10/2023.
- Modified by John Woolsey on 12/18/2023.

Copyright (c) 2023 Woolsey Workshop.  All rights reserved.

Members
-------
"""


# Imports
import logging
from arduino_iot_cloud import ArduinoCloudClient
from gpiozero import Button, LED

try:
    import secrets
except ImportError:
    print("Secrets are stored in secrets.py.")
    raise


# Global Constants
DEBUG: bool = True
"""The mode of operation; `False` = normal, `True` = debug."""


# Global Instances
button: Button = Button(5)
"""The momentary push button instance."""

led: LED = LED(21)
"""The LED instance."""

cloud_client: ArduinoCloudClient = None
"""The Arduino Cloud client instance."""


# Functions
def configure_cloud_client() -> None:
    """Configures the Arduino Cloud client."""

    global cloud_client
    cloud_client = ArduinoCloudClient(
        device_id=secrets.cloud["device_id"],
        username=secrets.cloud["device_id"],
        password=secrets.cloud["secret_key"],
    )
    cloud_client.register(
        "button_state",
        value=button.is_pressed,  # read and initialize button state
    )
    cloud_client.register("debug_message", value=None)
    cloud_client.register(
        "led_state",
        value=None,  # LED state is automatically initialized
        on_write=led_state_changed,  # call led_state_changed() on a change in value
    )


def configure_logging() -> None:
    """Configures logging used by the Arduino Cloud client."""

    if DEBUG:
        logging.basicConfig(
            datefmt="%H:%M:%S",
            format="%(asctime)s.%(msecs)03d %(message)s",
            level=logging.INFO,  # DEBUG, INFO, WARNING, etc.
        )


def button_pressed() -> None:
    """The callback function that executes each time the button is pressed."""

    cloud_client["button_state"] = True
    if DEBUG:
        print_debug_message("Button pressed.")


def button_released() -> None:
    """The callback function that executes each time the button is released."""

    cloud_client["button_state"] = False
    if DEBUG:
        print_debug_message("Button released.")


def led_state_changed(client: ArduinoCloudClient, value: bool) -> None:
    """The callback function that executes each time the `led_state` cloud
    variable is updated in the dashboard.

    :param ArduinoCloudClient client: The Arduino Cloud client instance.
    :param bool value: The new statue of the `led_state` cloud variable.
    """

    led.on() if value else led.off()
    if DEBUG:
        print_debug_message(f"Turned {'on' if value else 'off'} LED.")


def print_debug_message(message: str) -> None:
    """Prints the specified debug message to the screen and updates the
    `debug_message` cloud variable with the message.

    :param str message: The debug message.
    """

    cloud_client["debug_message"] = message
    print(message)


def main() -> None:
    """The main program entry."""

    configure_logging()
    configure_cloud_client()

    # Configure button callback functions
    button.when_pressed = button_pressed
    button.when_released = button_released

    if DEBUG:
        print_debug_message("DEBUG mode is enabled.")
    else:
        print_debug_message("DEBUG mode is disabled.")
    print("Press CTRL-C to exit.")

    # Start the Arduino Cloud client and keep the cloud variables synchronized
    cloud_client.start()  # endless loop


if __name__ == "__main__":  # required for generating Sphinx documentation
    main()
