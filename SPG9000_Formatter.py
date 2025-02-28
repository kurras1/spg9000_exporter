#------------------------------------------------------------------#
# SPG9000_Formatter.py                                             #
#                                                                  #
# Author:        Mike Kurras                                       #
# Date:          2/27/2025                                         #
# Description:   OpenMetrics exporter for Telestream SPG9000 Sync  #
#                Pulse Generator.                                  #
#                Designed for use with Prometheus                  #
#------------------------------------------------------------------#

import SPG9000_Enum_Data as enums

def build_metric_block(metrics):
    metric_block = "\n".join(metrics)
    return metric_block

#------------------------------------------------------------------#
#Format /system/status schema into Prometheus Formatting
#------------------------------------------------------------------#
def format_system_status(data):
    metrics = []
    
    #spg9000_num_faults
    metrics.append(f'# HELP spg9000_num_faults Number of active faults on the SPG9000')
    metrics.append(f'# TYPE spg9000_num_faults gauge')
    metrics.append(f'spg9000_num_faults {len(data["faults"])}')
    
    
    #spg9000_num_alerts
    metrics.append(f'# HELP spg9000_num_alerts Number of active alerts on the SPG9000')
    metrics.append(f'# TYPE spg9000_num_alerts gauge')
    metrics.append(f'spg9000_num_alerts {len(data["alerts"])}')
    
    #spg9000_led_state
    metrics.append(f'# HELP spg9000_led_state State of LED Lights on the SPG9000 {enums.systemLEDState}')
    metrics.append(f'# TYPE spg9000_led_state gauge')
    for led in data['leds']:
        metrics.append(f'spg9000_led_state{{led=\"{led}\"}} {enums.systemLEDState[data["leds"][led]]}')
    
    return build_metric_block(metrics)

#------------------------------------------------------------------#
#Format /system/health schema into Prometheus Formatting
#------------------------------------------------------------------#
def format_system_health(data):
    metrics = []
    
    system_cpu = data["main"]
        
    #spg9000_uptime
    metrics.append(f'# HELP spg9000_uptime Number of seconds since the system was powered-on')
    metrics.append(f'# TYPE spg9000_uptime counter')
    metrics.append(f'spg9000_uptime {system_cpu["uptime"]}')
    
    #spg9000_cpu_load_1min
    metrics.append(f'# HELP spg9000_cpu_load_1min CPU load average for the past 1 minute')
    metrics.append(f'# TYPE spg9000_cpu_load_1min gauge')
    metrics.append(f'spg9000_cpu_load_1min {system_cpu["cpu-load"]["avg-1min"]}')
    
    #spg9000_memory_total
    metrics.append(f'# HELP spg9000_memory_total Amount of memory total (in kibibyes)')
    metrics.append(f'# TYPE spg9000_memory_total gauge')
    metrics.append(f'spg9000_memory_total {system_cpu["memory"]["total"]}')
    
    #spg9000_memory_used
    metrics.append(f'# HELP spg9000_memory_used Amount of memory used (in kibibyes)')
    metrics.append(f'# TYPE spg9000_memory_used gauge')
    metrics.append(f'spg9000_memory_used {system_cpu["memory"]["used"]}')
    
    #spg9000_disk_total
    metrics.append(f'# HELP spg9000_disk_total Disk total for the eMMC storage device (in 1K blocks)')
    metrics.append(f'# TYPE spg9000_disk_total gauge')
    metrics.append(f'spg9000_disk_total {system_cpu["disk"]["total"]}')
    
    #spg9000_disk_used
    metrics.append(f'# HELP spg9000_disk_used Disk usage for the eMMC storage device (in 1K blocks)')
    metrics.append(f'# TYPE spg9000_disk_used gauge')
    metrics.append(f'spg9000_disk_used {system_cpu["disk"]["used"]}')
    
    return build_metric_block(metrics)

#------------------------------------------------------------------#
#Format /ptp/{instance} schema into Prometheus Formatting
#------------------------------------------------------------------#
def format_ptp_status(data):
    metrics = []
    
    ptp_status_data = {}

    for instance in data:
        
        instance_data = {}
        
        instance_data.update({"domain_number": data[instance]['default-ds']['domain-number']})
        instance_data.update({"instance_enable": (1 if "True" in str(data[instance]['default-ds']['instance-enable']) else 0)})
        instance_data.update({"priority1": ("NaN" if "None" in str(data[instance]['default-ds']['priority1']) else data[instance]['default-ds']['priority1'])})
        instance_data.update({"priority2": ("NaN" if "None" in str(data[instance]['default-ds']['priority2']) else data[instance]['default-ds']['priority2'])})
        instance_data.update({"port-state": data[instance]['port-ds-list'][0]['port-ds']['port-state']})

        ptp_status_data.update({instance: instance_data})
    
    #spg9000_ptp_domain_number
    metrics.append("# HELP spg9000_ptp_domain_number Currently configured PTP domain number")
    metrics.append("# TYPE spg9000_ptp_domain_number gauge")
    metrics.append(f'spg9000_ptp_domain_number{{interface=\"ptp1\"}} {ptp_status_data["1"]["domain_number"]}')
    metrics.append(f'spg9000_ptp_domain_number{{interface=\"ptp2\"}} {ptp_status_data["2"]["domain_number"]}')
    
    #spg9000_ptp_enable
    metrics.append("# HELP spg9000_ptp_enable Enabled state of PTP interface")
    metrics.append("# TYPE spg9000_ptp_enable gauge")
    metrics.append(f'spg9000_ptp_enable{{interface=\"ptp1\"}} {ptp_status_data["1"]["instance_enable"]}')
    metrics.append(f'spg9000_ptp_enable{{interface=\"ptp2\"}} {ptp_status_data["2"]["instance_enable"]}')
    
    #spg9000_ptp_priority1
    metrics.append("# HELP spg9000_ptp_priority1 Current value of PTP Priority 1 for interface")
    metrics.append("# TYPE spg9000_ptp_priority1 gauge")
    metrics.append(f'spg9000_ptp_priority1{{interface=\"ptp1\"}} {ptp_status_data["1"]["priority1"]}')
    metrics.append(f'spg9000_ptp_priority1{{interface=\"ptp2\"}} {ptp_status_data["2"]["priority1"]}')
    
    #spg9000_ptp_priority2
    metrics.append("# HELP spg9000_ptp_priority2 Current value of PTP Priority 2 for interface")
    metrics.append("# TYPE spg9000_ptp_priority2 gauge")
    metrics.append(f'spg9000_ptp_priority2{{interface=\"ptp1\"}} {ptp_status_data["1"]["priority2"]}')
    metrics.append(f'spg9000_ptp_priority2{{interface=\"ptp2\"}} {ptp_status_data["2"]["priority2"]}')
    
    #spg9000_ptp_state
    metrics.append(f'# HELP spg9000_ptp_state Current state of PTP interface {enums.port_ds_port_state}')
    metrics.append("# TYPE spg9000_ptp_state gauge")
    metrics.append(f'spg9000_ptp_state{{interface=\"ptp1\"}} {enums.port_ds_port_state[ptp_status_data["1"]["port-state"]]}')
    metrics.append(f'spg9000_ptp_state{{interface=\"ptp2\"}} {enums.port_ds_port_state[ptp_status_data["2"]["port-state"]]}')
    
    return build_metric_block(metrics)

#------------------------------------------------------------------#
#Format /Reference/Status schema into Prometheus Formatting
#------------------------------------------------------------------#
def format_reference_status(data):
    metrics = []
    
    #------------------------SYSTEM TIME------------------
    system_time = data['system-time']

    #spg9000_program_time
    metrics.append("# HELP spg9000_program_time The current program time of the SPG9000")
    metrics.append("# TYPE spg9000_program_time counter")
    program_time = sum(int(x) * 60 ** i for i, x in enumerate(reversed(system_time["program-time"].split(":"))))
    metrics.append(f'spg9000_program_time {program_time}')
    
    
    #------------------------GNSS STATUS------------------
    gnss_status = data['gnss']
    
    #spg9000_gnss_figure_of_merit
    metrics.append("# HELP spg9000_gnss_figure_of_merit Quality of the received GNSS Signal [Min 0, Max 9]")
    metrics.append("# TYPE spg9000_gnss_figure_of_merit gauge")
    metrics.append(f'spg9000_gnss_figure_of_merit {gnss_status["figure-of-merit"]}')
    
    #spg9000_satellites_in_fix
    metrics.append("# HELP spg9000_satellites_in_fix Current number of satellites locked to receiver")
    metrics.append("# TYPE spg9000_satellites_in_fix gauge")
    metrics.append(f'spg9000_satellites_in_fix {gnss_status["satellites-in-fix"]}')
    
    #spg9000_satellites_in_view
    metrics.append("# HELP spg9000_satellites_in_view Current number of satellites visible to receiver")
    metrics.append("# TYPE spg9000_satellites_in_view gauge")
    metrics.append(f'spg9000_satellites_in_view {gnss_status["satellites-in-view"]}')
    
    #spg9000_signal_quality
    metrics.append("# HELP spg9000_signal_quality Higher is better")
    metrics.append("# TYPE spg9000_signal_quality gauge")
    metrics.append(f'spg9000_signal_quality {gnss_status["signal-quality"]}')
    
    #spg9000_gnss_status
    metrics.append(f'# HELP spg9000_gnss_status Current Status of GNSS Receiver {enums.referenceStatus_gnss}')
    metrics.append("# TYPE spg9000_gnss_status gauge")
    metrics.append(f'spg9000_gnss_status {enums.referenceStatus_gnss[gnss_status["status"]]}')
    
    #------------------------REFERENCE SOURCE------------------
    reference_source = data['reference-source']
    metrics.append(f'# HELP spg9000_reference_source Current Source of Reference {enums.reference_source}')
    metrics.append("# TYPE spg9000_reference_source gauge")
    metrics.append(f'spg9000_reference_source {enums.reference_source[reference_source]}')
    
    return build_metric_block(metrics)
    
    