# Project Sundial

Project Sundial is a Python-based GUI application designed to control a device for SEE (Single Event Effects) radiation testing of space-grade power electronic products. The system automates hardware positioning and instrumentation connection using stepper and servo motors. The GUI facilitates user-friendly control and configuration of the device over a reliable Ethernet or Bluetooth connection.

## Features

- **PyQt5-based GUI**: Provides an intuitive interface for controlling and configuring the device.
- **Motor Control**: Executes precise control of motors using the `pigpiod` library.
- **SSH Integration**: Securely connects to a Raspberry Pi for remote command execution using `paramiko`.
- **Dynamic Input Parameters**: Accepts customizable parameters like total ICs, gear ratio, and steps per rotation.
- **Extensive Logging**: Displays real-time logs for user actions and system responses.
- **Error Handling**: Offers robust error handling and informative feedback.

## Installation

### Prerequisites
1. **Python 3.8+**
2. **Required Libraries**:
   - `PyQt5`
   - `paramiko`
   - `pigpiod` (on Raspberry Pi)

3. **Hardware Setup**:
   - Raspberry Pi 3 Model B+
   - Ethernet or Bluetooth connectivity
   - Stepper and servo motors

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/AaronElk4124/ProjectSundial.git
   cd ProjectSundial
