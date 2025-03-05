#------------------------------------------------------------------#
# SPG9000_Enum_Data.py                                             #
#                                                                  #
# Author:        Mike Kurras                                       #
# Date:          3/5/2025                                         #
# Description:   OpenMetrics exporter for Telestream SPG9000 Sync  #
#                Pulse Generator.                                  #
#                Designed for use with Prometheus                  #
#------------------------------------------------------------------#


#------------------------------------------------------------------#
#ENUM Data for API Returns from SPG9000
#------------------------------------------------------------------#

#ENUM For satellite-receiver-status-ds
satellite_receiver_status_ds = {
    "no-signal": 1, 
    "low-signal": 2, 
    "acquiring-satellites": 3, 
    "unusable-signal": 4, 
    "acquiring-position": 5, 
    "establishing-fix": 6, 
    "locked": 7, 
    "locked-min": 8, 
    "locked-nominal": 9, 
    "locked-strong": 10
}
#ENUM for referenceStatus_gnss
referenceStatus_gnss = {
    "unlocked": 1, 
    "acquiring-satellites": 2, 
    "bad-position": 3, 
    "acquiring-position": 4, 
    "adjusting-phase": 5, 
    "locked-warning": 6, 
    "locked-min": 7, 
    "locked-nominal": 8, 
    "locked-strong": 9
}
#ENUM for referenceStatus_ptpfollower
referenceStatus_ptpfollower = {
    "unlocked": 1, 
    "listening": 2, 
    "setting-time": 3, 
    "adjusting-phase": 4, 
    "locked-1000ns": 5, 
    "locked-250ns": 6, 
    "locked-100ns": 7, 
    "locked-50ns": 8
}
#ENUM for referenceSouce
reference_source = {
    "primary": 1, 
    "secondary": 2, 
    "holdover": 3
}
#ENUM for port-ds/port-state
port_ds_port_state = {
    "initializing": 1, 
    "faulty": 2, 
    "disabled": 3, 
    "listening": 4, 
    "pre-master": 5, 
    "master": 6, 
    "passive": 7, 
    "uncalibrated": 8, 
    "slave": 9
}
#ENUM for systemLEDState
systemLEDState = {
    "off": 0, 
    "green": 1, 
    "amber": 2, 
    "red": 3, 
    "dim-green": 4, 
    "dim-amber": 5, 
    "dim-red": 6, 
    "blink-green": 7, 
    "blink-amber": 8, 
    "blink-red": 9
}