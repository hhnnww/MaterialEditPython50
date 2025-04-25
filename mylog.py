"""sets up a logger for the MaterialEdit class."""

import logging

# Configure the logger
mylogger = logging.getLogger("MaterialEditLogger")
mylogger.setLevel(logging.INFO)

# Create a console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Create a formatter and set it for the handler
formatter = logging.Formatter("")
console_handler.setFormatter(formatter)

# Add the handler to the logger
mylogger.addHandler(console_handler)
