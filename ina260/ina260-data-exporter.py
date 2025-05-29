import time
import logging

from prometheus_client import start_http_server, Gauge
import argparse
import socket
import board
import adafruit_ina260

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('--address', type=int, default=0x40)
arg_parser.add_argument('--hostname', type=str, default=socket.gethostname())
arg_parser.add_argument('--device', type=str, default='deepx')
arg_parser.add_argument('--port', type=int, default=8000)
args = arg_parser.parse_args()

logging.basicConfig(level=logging.INFO)
# Initialize INA260 Sensor
i2c = board.I2C()
ina260 = adafruit_ina260.INA260(i2c, args.address)

# Get hostname
hostname = args.hostname
device = args.device
# Create Prometheus metrics
voltage_gauge = Gauge('ina260_voltage', 'Voltage measured by INA260', ['hostname', 'device'])
current_gauge = Gauge('ina260_current', 'Current measured by INA260', ['hostname', 'device'])
power_gauge = Gauge('ina260_power', 'Power measured by INA260', ['hostname', 'device'])

def collect_metrics():
    while True:
        # Read voltage and current from INA260
        try:
            voltage = ina260.voltage
            current = ina260.current
            power = ina260.power

            # Update Prometheus metrics
            voltage_gauge.labels(hostname, device).set(voltage)
            current_gauge.labels(hostname, device).set(current)
            power_gauge.labels(hostname, device).set(power)

            # Sleep for a bit before collecting metrics again
            print(f"Voltage: {voltage}, Current: {current}, Power: {power}")
            time.sleep(1)
        except OSError as e:
            # Current out of device range with specified shunt resistor
            print(e)
            time.sleep(1)
        except Exception as e:
            # Current out of device range with specified shunt resistor
            print(e)
            time.sleep(1)



if __name__ == '__main__':
    # Start Prometheus HTTP server on port 8000(default, can be changed using --port argument)
    logging.info("Start INA260 Log Collector on " + str(args.port))
    start_http_server(args.port)
    # Start collecting metrics
    collect_metrics()
