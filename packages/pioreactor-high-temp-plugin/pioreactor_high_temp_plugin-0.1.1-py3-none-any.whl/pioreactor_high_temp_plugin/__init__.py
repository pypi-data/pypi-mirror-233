from pioreactor.background_jobs.monitor import Monitor

try:
    from temperature_expansion_kit_plugin import Thermostat
except ImportError:
    from pioreactor.automations.temperature.thermostat import Thermostat

try:
    from temperature_expansion_kit_plugin import TemperatureControllerWithProbe as TemperatureController
except ImportError:
    from pioreactor.background_jobs.temperature_control import TemperatureController


TemperatureController.MAX_TEMP_TO_REDUCE_HEATING = 81.5
TemperatureController.MAX_TEMP_TO_DISABLE_HEATING = 83.5
TemperatureController.MAX_TEMP_TO_SHUTDOWN = 85.0

TemperatureController.INFERENCE_EVERY_N_SECONDS = 5 * 60 # PWM is on for just over half the time, instead of ~1/3

Monitor.MAX_TEMP_TO_SHUTDOWN = 85.0
Thermostat.MAX_TARGET_TEMP = 90.0

