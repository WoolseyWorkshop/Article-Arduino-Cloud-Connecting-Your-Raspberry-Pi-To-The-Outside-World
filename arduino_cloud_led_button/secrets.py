"""The secrets file.

Description
-----------

- Contains the secrets used for accessing the Arduino Cloud service.

Notes
-----

- Replace the secret placeholders with the values appropriate for your setup.
- Comments are Sphinx (reStructuredText) compatible.

TODO
----

- None.

Author(s)
---------

- Created by John Woolsey on 11/10/2023.
- Modified by John Woolsey on 11/19/2023.

Copyright (c) 2023 Woolsey Workshop.  All rights reserved.

Members
-------
"""


# Arduino Cloud
cloud: dict[str, str] = {
    "device_id": "your_device_id",
    "secret_key": "your_secret_key",
}
"""Dictionary containing secrets for accessing the Arduino Cloud service.

:param str device_id: The unique device ID for the Raspberry Pi.
:param str secret_key: The secret key for authorized access to the Arduino Cloud
    service.
"""
