CREATE TABLE nestbase (
_id STRING, 
display_name STRING,
device_type STRING,
device_status STRING,
fan_timer_mode STRING,
thermostat_mode STRING,
eco_mode STRING
eco_heat_max_cel DECIMAL(6),
eco_cool_min_cel DECIMAL(6),
hvac_status STRING,
temp_display_unit STRING,
therm_heat_max_cel DECIMAL(6),
therm_cool_min_cel DECIMAL(6),
humidity_pct INT,
ambient_temp_cel DECIMAL(6),
measurement_ts TIMESTAMP
);

