# rbp-controller

## Description
This repository contains a Python script designed to collect and export data from an INA260 power sensor connected via an I2C multiplexer (TCA9548A). The script exposes the collected data as Prometheus metrics, allowing for real-time monitoring of voltage, current, and power measurements.

## ina260/ina260-data-expoter.py
This Python script is designed to collect voltage, current, and power measurements from an INA260 sensor and expose them as Prometheus metrics via an HTTP server. It also incorporates an I2C multiplexer (TCA9548A) to allow multiple I2C devices on the same bus or to select a specific channel for the INA260.

Here's a breakdown of what the code does:

1.  **Imports necessary libraries:**
    *   `time`: For pausing execution (`time.sleep`).
    *   `logging`: For logging informational messages and errors.
    *   `prometheus_client`: To create and expose Prometheus metrics (`start_http_server`, `Gauge`).
    *   `argparse`: For parsing command-line arguments.
    *   `socket`: To get the hostname of the machine.
    *   `board`: From `busio` or similar, provides access to hardware I2C pins.
    *   `adafruit_ina260`: Library for interacting with the INA260 sensor.
    *   `adafruit_tca9548a`: Library for interacting with the TCA9548A I2C multiplexer.

2.  **Argument Parsing:**
    *   It sets up an `ArgumentParser` to accept command-line arguments:
        *   `--address`: The I2C address of the TCA9548A multiplexer (default: `0x70`).
        *   `--hostname`: The hostname to use for Prometheus labels (default: actual machine hostname).
        *   `--device`: A device identifier for Prometheus labels (default: `'deepx'`).
        *   `--port`: The HTTP port for the Prometheus server (default: `8000`).
        *   `--channel`: The TCA9548A channel where the INA260 is connected (default: `7`).

3.  **Logging Configuration:**
    *   Sets up basic logging to display `INFO` level messages and above.

4.  **I2C Bus and TCA9548A Multiplexer Initialization:**
    *   Initializes the I2C bus using `board.I2C()`.
    *   Attempts to initialize the `adafruit_tca9548a.TCA9548A` multiplexer using the provided I2C address.
    *   Includes error handling: if the multiplexer is not found at the specified address, it logs an error and exits.

5.  **INA260 Sensor Initialization:**
    *   Selects a specific channel on the TCA9548A multiplexer (`tca[INA260_CHANNEL]`) where the INA260 sensor is expected to be connected. This is crucial because the multiplexer allows routing the I2C communication to one of its 8 channels.
    *   Attempts to initialize the `adafruit_ina260.INA260` sensor through the selected multiplexer channel.
    *   Includes error handling: if the INA260 sensor is not found on that channel or at that address, it logs an error and exits.

6.  **Prometheus Metrics Setup:**
    *   Retrieves the hostname and device name (either from arguments or system).
    *   Creates three Prometheus `Gauge` metrics:
        *   `ina260_voltage`: For voltage measurements.
        *   `ina260_current`: For current measurements.
        *   `ina260_power`: For power measurements.
    *   Each gauge has labels `['hostname', 'device']`, allowing Prometheus to differentiate metrics from different hosts or devices.

7.  **`collect_metrics` Function (Data Collection Loop):**
    *   This function runs in an infinite loop (`while True`).
    *   Inside the loop:
        *   It reads the `voltage`, `current`, and `power` properties directly from the initialized `ina260` object. The `adafruit_ina260` library handles the I2C communication and data conversion internally.
        *   It updates the corresponding Prometheus gauges using `voltage_gauge.labels(hostname, device).set(voltage)`, etc.
        *   It logs the read values to the console.
        *   It pauses for 1 second (`time.sleep(1)`) before the next reading.
        *   It includes robust error handling using `try-except` blocks to catch `OSError` (e.g., I2C communication issues) or any other unexpected exceptions, logging them and retrying after a short delay.

8.  **Main Execution Block (`if __name__ == '__main__':`)**
    *   When the script is run directly:
        *   It starts an HTTP server on the specified port (`args.port`) using `start_http_server()`. This server will serve the Prometheus metrics at the `/metrics` endpoint (e.g., `http://your-ip:8000/metrics`).
        *   It then calls the `collect_metrics()` function, which starts the continuous data collection and metric exposure loop.

In summary, this script acts as an **I2C sensor data exporter** that reads power monitoring data (voltage, current, power) from an INA260 sensor connected via a TCA9548A I2C multiplexer and makes this data available for monitoring systems like Prometheus.
