#!/usr/bin/python

# icon set
# choose between small and medium or define your own set
ICON_SET = "small"

# voltage steps for small icon set
VOLT_STEPS_SMALL =	[
					[ 100, 4.1, "small/battery100.png" ],
					[ 90, 4.0, "small/battery90.png" ],
					[ 80, 3.9, "small/battery80.png" ],
					[ 70, 3.8, "small/battery70.png" ],
					[ 60, 3.7, "small/battery60.png" ],
					[ 50, 3.6, "small/battery50.png" ],
					[ 40, 3.5, "small/battery40.png" ],
					[ 30, 3.4, "small/battery30.png" ],
					[ 20, 3.3, "small/battery20.png" ],
					[ 10, 3.2, "small/battery10.png" ]
					]

# icon location for small icon set
ICON_X_SMALL = 463
ICON_Y_SMALL = 2

# voltage steps for medium icon set
VOLT_STEPS_MEDIUM =	[
					[ 100, 4.1, "medium/battery100.png" ],
					[ 90, 4.0, "medium/battery90.png" ],
					[ 80, 3.9, "medium/battery80.png" ],
					[ 70, 3.8, "medium/battery70.png" ],
					[ 60, 3.7, "medium/battery60.png" ],
					[ 50, 3.6, "medium/battery50.png" ],
					[ 40, 3.5, "medium/battery40.png" ],
					[ 30, 3.4, "medium/battery30.png" ],
					[ 20, 3.3, "medium/battery20.png" ],
					[ 10, 3.2, "medium/battery10.png" ]
					]

# icon location for medium icon set
ICON_X_MEDIUM = 448
ICON_Y_MEDIUM = 2

# selected icon set
if (ICON_SET == "small"):
	VOLT_STEPS = VOLT_STEPS_SMALL
	ICON_X = ICON_X_SMALL
	ICON_Y = ICON_Y_SMALL
elif (ICON_SET == "medium"):
	VOLT_STEPS = VOLT_STEPS_MEDIUM
	ICON_X = ICON_X_MEDIUM
	ICON_Y = ICON_Y_MEDIUM
else:
	# default icosn set
	VOLT_STEPS = VOLT_STEPS_SMALL
	ICON_X = ICON_X_SMALL
	ICON_Y = ICON_Y_SMALL

# path to pngview (raspidmx)
PNGVIEW_PATH = "/home/pi/raspidmx/pngview"

# path to icons
ICON_PATH = "batmon/icons"

# refresh rate (s)
REFRESH_RATE = 10

# display debug messages
DEBUG_MSG = 0

# create CSV output for logging
CSV_OUT = 0

# DispmanX layer
DISPMANX_BASE_LAYER = 20000