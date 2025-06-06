import time
import logging

from prometheus_client import start_http_server, Gauge
import argparse
import socket
import board
import adafruit_ina260
import adafruit_tca9548a # Import the TCA9548A library

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('--address', type=int, default=0x70)
arg_parser.add_argument('--hostname', type=str, default=socket.gethostname())
arg_parser.add_argument('--device', type=str, default='deepx')
arg_parser.add_argument('--port', type=int, default=8000)
arg_parser.add_argument('--channel', type=int, default=7, help='TCA9548A channel to use for INA260 (0-7)')
args = arg_parser.parse_args()

logging.basicConfig(level=logging.INFO)

# Initialize I2C bus
i2c = board.I2C()

# TCA9548A multiplexer address
TCA9548A_ADDRESS = args.address
logging.info(f"Using TCA9548A multiplexer with I2C address: 0x{TCA9548A_ADDRESS:x}")
# Initialize TCA9548A multiplexer
try:
    tca = adafruit_tca9548a.TCA9548A(i2c, address=TCA9548A_ADDRESS)
    logging.info(f"TCA9548A multiplexer initialized at address 0x{TCA9548A_ADDRESS:x}")
except ValueError:
    logging.error(f"Could not find a TCA9548A at address 0x{TCA9548A_ADDRESS:x}. Please check wiring or address configuration.")
    exit(1)
# Assuming INA260 is connected to channel 7 of the TCA9548A.
# You can change this to tca[1], tca[2], etc., if connected to a different channel.
INA260_CHANNEL = args.channel

# Initialize INA260 Sensor via the selected TCA9548A channel
try:
    logging.info(f"Initializing INA260 on TCA9548A channel {INA260_CHANNEL} with address 0x{args.address:x}")
    ina260 = adafruit_ina260.INA260(tca[INA260_CHANNEL])
    logging.info(f"INA260 sensor initialized on TCA9548A channel {INA260_CHANNEL} with address 0x{args.address:x}")
except ValueError:
    logging.error(f"Could not find an INA260 sensor on TCA9548A channel {INA260_CHANNEL} at address 0x{args.address:x}. Please check wiring or address configuration.")
    exit(1)


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
            # The INA260 object already encapsulates the channel selection through `tca[INA260_CHANNEL]`
            voltage = ina260.voltage
            current = ina260.current
            power = ina260.power

            # Update Prometheus metrics
            voltage_gauge.labels(hostname, device).set(voltage)
            current_gauge.labels(hostname, device).set(current)
            power_gauge.labels(hostname, device).set(power)

            # Sleep for a bit before collecting metrics again
            logging.info(f"Voltage: {voltage:.2f}V, Current: {current:.2f}mA, Power: {power:.2f}mW")
            time.sleep(1)
        except OSError as e:
            # Handle I/O errors, e.g., device not found or communication issue
            logging.error(f"OSError: {e}. Retrying in 1 second.")
            time.sleep(1)
        except Exception as e:
            # Catch any other unexpected errors
            logging.error(f"An unexpected error occurred: {e}. Retrying in 1 second.")
            time.sleep(1)



if __name__ == '__main__':
    # Start Prometheus HTTP server on port 8000(default, can be changed using --port argument)
    logging.info(f"Starting INA260 Log Collector on port {args.port}")
    start_http_server(args.port)
    # Start collecting metrics
    collect_metrics()
