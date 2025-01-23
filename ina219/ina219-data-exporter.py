import time

from ina219 import INA219, DeviceRangeError
from prometheus_client import start_http_server, Gauge
import random
import argparse
import socket
arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('--shunt_ohms', type=float, default=0.1)
arg_parser.add_argument('--max_expected_amps', type=float, default=0.1)
arg_parser.add_argument('--address', type=int, default=0x40)
arg_parser.add_argument('--hostname', type=str, default=socket.gethostname())
arg_parser.add_argument('--device', type=str, default='deepx')
arg_parser.add_argument('--port', type=int, default=8000)
args = arg_parser.parse_args()
# Initialize INA219 sensor
ina = INA219(shunt_ohms=args.shunt_ohms, max_expected_amps=args.max_expected_amps, address=args.address)
ina.configure()

# Get hostname
hostname = args.hostname
device = args.device
# Create Prometheus metrics
voltage_gauge = Gauge('ina219_voltage', 'Voltage measured by INA219', ['hostname', 'device'])
supply_voltage_gauge = Gauge('ina219_supply_voltage', 'Supply Voltage measured by INA219', ['hostname', 'device'])
shunt_voltage_gauge = Gauge('ina219_shunt_voltage', 'Shunt Voltage measured by INA219', ['hostname', 'device'])
current_gauge = Gauge('ina219_current', 'Current measured by INA219', ['hostname', 'device'])
power_gauge = Gauge('ina219_power', 'Power measured by INA219', ['hostname', 'device'])

voltage_gauge.labels('hostname', hostname)
supply_voltage_gauge.labels('hostname', hostname)
def collect_metrics():
    while True:
        # Read voltage and current from INA219
        try:
            voltage = ina.voltage()
            supply_voltage = ina.supply_voltage()
            shunt_voltage = ina.shunt_voltage()
            current = ina.current()
            power = ina.power()

            # Update Prometheus metrics
            voltage_gauge.labels(hostname, device).set(voltage)
            supply_voltage_gauge.labels(hostname, device).set(supply_voltage)
            shunt_voltage_gauge.labels(hostname, device).set(shunt_voltage)
            current_gauge.labels(hostname, device).set(current)
            power_gauge.labels(hostname, device).set(power)

            # Sleep for a bit before collecting metrics again
            time.sleep(1)
        except DeviceRangeError as e:
            # Current out of device range with specified shunt resistor
            print(e)
            time.sleep(1)


if __name__ == '__main__':
    # Start Prometheus HTTP server on port 8000(default, can be changed using --port argument)
    start_http_server(args.port)
    # Start collecting metrics
    collect_metrics()