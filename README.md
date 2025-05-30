# rbp-controller

## Description
This repository contains a Python script designed to collect and export data from an INA260 power sensor. The script exposes the collected data as Prometheus metrics, allowing for real-time monitoring of voltage, current, and power measurements.

## ina260/ina260-data-expoter.py
This Python script is designed to collect voltage, current, and power measurements from an INA260 sensor and expose them as Prometheus metrics via an HTTP server.

Here's a breakdown of what the code does:

1.  **Imports necessary libraries:**
    *   `time`: For pausing execution (`time.sleep`).
    *   `logging`: For logging informational messages and errors.
    *   `prometheus_client`: To create and expose Prometheus metrics (`start_http_server`, `Gauge`).
    *   `argparse`: For parsing command-line arguments.
    *   `socket`: To get the hostname of the machine.
    *   `board`: From `busio` or similar, provides access to hardware I2C pins.
    *   `adafruit_ina260`: Library for interacting with the INA260 sensor.

2.  **Argument Parsing:**
    *   It sets up an `ArgumentParser` to accept command-line arguments:
        *   `--hostname`: The hostname to use for Prometheus labels (default: actual machine hostname).
        *   `--device`: A device identifier for Prometheus labels (default: `'deepx'`).
        *   `--port`: The HTTP port for the Prometheus server (default: `8000`).

3.  **Logging Configuration:**
    *   Sets up basic logging to display `INFO` level messages and above.

4.  **I2C Bus Initialization:**
    *   Initializes the I2C bus using `board.I2C()`.

5.  **INA260 Sensor Initialization:**
    *   Attempts to initialize the `adafruit_ina260.INA260` sensor.
    *   Includes error handling: if the INA260 sensor is not found, it logs an error and exits.

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

In summary, this script acts as an **I2C sensor data exporter** that reads power monitoring data (voltage, current, power) from an INA260 sensor and makes this data available for monitoring systems like Prometheus.
