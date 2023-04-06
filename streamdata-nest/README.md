# Streaming your personal nest

There comes a point in testing data products when you become sick of using synthetic data and whatever you can find lying around on Kaggle. If you hit that point and start looking around your apartment for something REAL, you may just spot a Nest thermostat. This is capable of generating real data that you can stream into FeatureBase. This repo will walk you through this process, but there are some pre-requisites.

## Before you begin

* Purchase and setup a Nest Thermostat
* [Follow these instructions](https://www.wouternieuwerth.nl/controlling-a-google-nest-thermostat-with-python/) to set up access to your nest data, which includes a purchase ($5) google developer access
* Have a [FeatureBase Cloud account](https://cloud.featurebase.com/signup)
* Have ready access to the following:
    * Nest Project ID
    * Nest access token
    * Nest refresh token
    * Nest client ID
    * FeatureBase username (email)
    * FeatureBase password
    * FeatureBase database id

All credit to the above blog for helping me get set up to access my nest's data!

## Setup python env

You need to have a python environment with the proper packages found in the requirements.txt

### Create using conda

```
conda create --name nestbase --file requirements.txt
```
## Start

If you’re reading this section, you’ve completed the steps above and should feel accomplished already! You’ve bitten the bullet and paid Google for your own data, but you can now do whatever you want with it! First off, you need to get the device you want to pull data from. You can make a call to the smart device endpoint with your project to see all available devices:

```python
def get_devices(self):
    """Get all of the devices in your nest project

    Returns:
        List: List of devices under your nest project
    """
    url_get_devices = 'https://smartdevicemanagement.googleapis.com/v1/enterprises/' + self.project_id + '/devices'
    response = requests.get(url_get_devices, headers=self.headers)

    return response.json()
```

 This walkthrough and code assumes you only have one thermostat device, but you can easily tweak the code to incorporate multiple devices if desired. 
 
 Once you have the correct device name, you can query it to get your device’s stats. This will return data that looks similar to the below payload:

```json
{
  "type" : "sdm.devices.types.THERMOSTAT",
  "traits" : {
    "sdm.devices.traits.Connectivity" : {
      "status" : "ONLINE"
    },
    "sdm.devices.traits.Fan" : {
      "timerMode" : "ON",
      "timerTimeout" : "2019-05-10T03:22:54Z"
    },
    "sdm.devices.traits.Humidity" : {
      "ambientHumidityPercent" : 35.0
    },
    "sdm.devices.traits.Info" : {
      "customName" : "My device"
    },
    "sdm.devices.traits.Settings" : {
      "temperatureScale" : "CELSIUS"
    },
    "sdm.devices.traits.Temperature" : {
      "ambientTemperatureCelsius" : 23.0
    },
    "sdm.devices.traits.ThermostatEco" : {
      "availableModes" : ["MANUAL_ECO", "OFF"],
      "mode" : "MANUAL_ECO",
      "heatCelsius" : 20.0,
      "coolCelsius" : 22.0
    },
    "sdm.devices.traits.ThermostatHvac" : {
      "status" : "HEATING"
    },
    "sdm.devices.traits.ThermostatMode" : {
      "availableModes" : ["HEAT", "COOL", "HEATCOOL", "OFF"],
      "mode" : "COOL"
    },
    "sdm.devices.traits.ThermostatTemperatureSetpoint" : {
      "heatCelsius" : 20.0,
      "coolCelsius" : 22.0
    }
  }
}
```
Detailed information about each trait can be found on [Google's docs](https://developers.google.com/nest/device-access/api/thermostat#json). 

## Data modeling in FeatureBase

With a preview of the data, it’s time to model the data in FeatureBase. You can create a DDL statement with the traits of interest. Below is an example statement with familiar data types that elects the time of the thermostat reading as the table’s primary key (_id):

```sql
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
```

After inspecting a record, you realize how dependent your brain is on seeing Fahrenheit over Celsius. After going down an internal rabbit hole on why there is a metric system and an imperial system and questioning why the world can’t just get along, you decide that you want the ambient temperature to also show in Fahrenheit, so you add that column to the table:

```sql
ALTER TABLE nestbase ADD ambient_temp_far DECIMAL(6);
```

## Loading data

You are now ready to load data. For FeatureBase you can use [BULK INSERT statements](https://docs.featurebase.com/docs/sql-guide/statements/statement-insert-bulk/), which allow you to stream JSON data into your table. `BULK INSERT` gives you the flexibility to send 1 to n records, but for the examples that follow, each record will be sent individually. `BULK INSERT` allows for light data manipulation in the [TRANSFORM clause](https://docs.featurebase.com/docs/sql-guide/statements/statement-insert-bulk/#transform-clause-1), so you implement the temperature conversion there. An example of sending one record can be seen below:

```sql
BULK INSERT INTO gt-nest-thermo (
_id, 
display_name,
device_type,
device_status,
fan_timer_mode,
thermostat_mode,
eco_mode,
eco_heat_max_cel,
eco_cool_min_cel,
hvac_status,
temp_display_unit,
therm_heat_max_cel,
therm_cool_min_cel,
ambient_humidity_pct,
ambient_temp_cel,
measurement_ts,
ambient_temp_far
)
MAP (
'$["req_time"]' TIMESTAMP,
'$["type"]' STRING,
'$["traits"]["sdm.devices.traits.Humidity"]["ambientHumidityPercent"]' INT,
'$["traits"]["sdm.devices.traits.Connectivity"]["status"]' STRING,
'$["traits"]["sdm.devices.traits.Fan"]["timerMode"]' STRING,
'$["traits"]["sdm.devices.traits.ThermostatMode"]["mode"]' STRING,
'$["traits"]["sdm.devices.traits.ThermostatEco"]["mode"]' STRING,
'$["traits"]["sdm.devices.traits.ThermostatEco"]["heatCelsius"]' DECIMAL(6),
'$["traits"]["sdm.devices.traits.ThermostatEco"]["coolCelsius"]' DECIMAL(6),
'$["traits"]["sdm.devices.traits.ThermostatHvac"]["status"]' STRING,
'$["traits"]["sdm.devices.traits.Settings"]["temperatureScale"]' STRING,
'$["traits"]["sdm.devices.traits.ThermostatTemperatureSetpoint"]["heatCelsius"]' DECIMAL(6),
'$["traits"]["sdm.devices.traits.ThermostatTemperatureSetpoint"]["coolCelsius"]' DECIMAL(6),
'$["traits"]["sdm.devices.traits.Temperature"]["ambientTemperatureCelsius"]' DECIMAL(6),
'$["parentRelations"][0]["displayName"]' STRING
)
TRANSFORM(
CAST(@0 as STRING),
@14,
@1,
@3,
@4,
@5,
@6,
@7,
@8,
@9,
@10,
@11,
@12,
@2,
@13,
@0,
(@13*9/5)+32)
FROM '<record>'
WITH
BATCHSIZE 10000
FORMAT 'NDJSON'
INPUT 'STREAM'
ALLOW_MISSING_VALUES;
```


## Putting it all together
You are happy with the data model and are officially ready to start streaming data. You want to set and forget this and have data keep loading, so you need a couple of things: a connection to your Nest, a connection to FeatureBase, a way to refresh your connections, and a method to constantly pull and push data. Luckily [the nestbase.py script](/nestbase.py) does that all for you. 

You are pretty smart, so you check the script out before running and find this will continuously run but only poll Nest every 6 seconds because Google limits device info to 10 QPM: https://developers.google.com/nest/device-access/project/limits . **Lastly, you correctly call into question the method in which secrets for Nest and FeatureBase are used and modify the script in accordance with your security needs.** You run the script (and use something like `caffeinate` when on a mac) and leave it be.


## Running the script
### Inputs
* Have ready access to the following:
    * Nest Project ID
    * Nest access token
    * Nest refresh token
    * Nest client ID
    * FeatureBase username (email)
    * FeatureBase password
    * FeatureBase database id

### With a nest refresh token and a specific FeatureBase database

`python nestbase.py --project_id <> --access_token <> --refresh_token <> --client_id <> --client_secret <> --fb_user <> --fb_pw <> --fb_db <>`

### With a token that will expire within an hour

`python nestbase.py --project_id <> --access_token <> --fb_user <> --fb_pw <> --fb_db <>`

## Analyze the data

A couple days later you can return to play around with your recently loaded data. You have a couple of questions you want to answer:

1. What does the temperature and humidity look like at my place over time
2. How variable is the temperature and humidity in my place?
3. How long does it take for my place to cool down to my desired temperature?
4. How often is my fan on during the day?
5. When does my A/C turn on in relation to its target temperature



