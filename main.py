import sys

import serial
import paramiko
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import pyqtSignal, QThread


class DeviceControlApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.log_text = None
        self.init_ui()
        self.serial_connection = None

    def init_ui(self):
        self.setWindowTitle("Project Sundial Control Panel")
        self.setGeometry(100, 100, 1000, 700)

        main_layout = QtWidgets.QHBoxLayout()

        control_panel = QtWidgets.QVBoxLayout()

        status_label = QtWidgets.QLabel("Device Status: Idle")
        status_label.setFont(QtGui.QFont("Arial", 18, QtGui.QFont.Bold))
        status_label.setAlignment(QtCore.Qt.AlignCenter)
        self.status_label = status_label
        control_panel.addWidget(status_label)

        parameters_group = QtWidgets.QGroupBox("Device Parameters")
        parameters_group.setStyleSheet(
            "QGroupBox { font-size: 16px; font-weight: bold; padding: 10px; border: 2px solid #4CAF50; border-radius: 5px; }"
        )
        parameters_layout = QtWidgets.QFormLayout()

        self.total_ics_input = self.create_input_field("Total ICs", parameters_layout)
        self.gear_ratio_input = self.create_input_field("Gear Ratio", parameters_layout)
        self.steps_per_rotation_input = self.create_input_field("Steps per Rotation", parameters_layout)
        self.ip_address_input = self.create_input_field("Raspberry Pi IP Address", parameters_layout)

        parameters_group.setLayout(parameters_layout)
        control_panel.addWidget(parameters_group)

        self.connect_button = self.create_button("Connect", "#2196F3", self.connect_to_pi)
        control_panel.addWidget(self.connect_button)

        button_layout = QtWidgets.QHBoxLayout()
        self.start_button = self.create_button("Start", "#4CAF50", self.start_device)
        self.stop_button = self.create_button("Stop", "#f44336", self.stop_device)
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.stop_button)
        control_panel.addLayout(button_layout)

        main_layout.addLayout(control_panel, 2)

        log_panel = QtWidgets.QVBoxLayout()

        log_label = QtWidgets.QLabel("Log")
        log_label.setFont(QtGui.QFont("Arial", 16, QtGui.QFont.Bold))
        log_panel.addWidget(log_label)

        self.log_text = QtWidgets.QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setStyleSheet("background-color: #f0f0f0; padding: 10px; border-radius: 5px; font-size: 14px;")
        log_panel.addWidget(self.log_text)

        main_layout.addLayout(log_panel, 1)

        self.setLayout(main_layout)

    def create_input_field(self, label_text, layout):
        label = QtWidgets.QLabel(label_text)
        label.setFont(QtGui.QFont("Arial", 16))
        input_field = QtWidgets.QLineEdit()

        input_field.setStyleSheet(
            """
            QLineEdit {
                padding: 10px;
                font-size: 18px;
                border: 2px solid #4CAF50;
                border-radius: 25px;
                background-color: #f9f9f9;
            }
            QLineEdit:focus {
                border-color: #2196F3;
                background-color: #e0f7fa;
            }
            """
        )
        input_field.setMinimumHeight(50)
        layout.addRow(label, input_field)
        return input_field

    def create_button(self, text, color, callback):
        button = QtWidgets.QPushButton(text)
        button.setStyleSheet(
            f"background-color: {color}; color: white; padding: 10px 20px; font-size: 16px; border-radius: 10px;"
        )
        button.setFixedHeight(50)
        button.clicked.connect(callback)
        return button

    hostname = "192.168.2.3"

    def connect_to_pi(self):
        try:
            hostname = self.ip_address_input.text().strip()
            if not hostname:
                self.log_message("Please enter a valid IP address.")
                return

            username = "team6"
            password = "team6"

            # Create an SSH client
            self.ssh_client = paramiko.SSHClient()
            self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            # Connect to the Raspberry Pi
            self.ssh_client.connect(hostname, username=username, password=password)
            self.log_message(f"Connected to Raspberry Pi at {hostname} via SSH")
            self.status_label.setText("Device Status: Connected")

        except paramiko.SSHException as e:
            self.log_message(f"Error connecting to Raspberry Pi via SSH: {e}")
            self.status_label.setText("Device Status: Error")

    def start_device(self):
        if hasattr(self, 'ssh_client') and self.ssh_client:
            try:
                # Get input values
                total_ics = float(self.total_ics_input.text())
                gear_ratio = float(self.gear_ratio_input.text())
                steps_per_rotation = float(self.steps_per_rotation_input.text())

                # Calculate and prepare the command
                command = "python3 /home/team6/Desktop/stepper_testing/Two_stepper_motors.py"
                self.log_message(f"Calculating IC: {steps_per_rotation * gear_ratio / total_ics}")

                # Execute the command on the Raspberry Pi
                stdin, stdout, stderr = self.ssh_client.exec_command(command)
                output = stdout.read().decode()
                error = stderr.read().decode()

                # Display command results
                if output:
                    self.log_message(f"Output: {output}")
                if error:
                    self.log_message(f"Error: {error}")

                self.status_label.setText("Device Status: Running")
            except ValueError:
                self.log_message("Please enter valid numbers in all fields.")
        else:
            self.log_message("Not connected to Raspberry Pi! Please press Connect.")


    # Modify stop_device to use StopDeviceThread
    def stop_device(self):
        if hasattr(self, 'ssh_client') and self.ssh_client:
            command = "pkill -f python3"
            stdin, stdout, stderr = self.ssh_client.exec_command(command, timeout=5)
            self.ssh_client.close()
            self.status_label.setText("Device Status: Stopping...")
        else:
            self.log_message("Not connected to Raspberry Pi!")

    def log_message(self, message):
        self.log_text.append(message)

    def resizeEvent(self, event):
        window_size = self.size()
        font_size = max(14, int(window_size.width() * 0.015))
        self.status_label.setFont(QtGui.QFont("Arial", font_size, QtGui.QFont.Bold))
        super(DeviceControlApp, self).resizeEvent(event)


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = DeviceControlApp()
    window.show()
    window.showMaximized()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()