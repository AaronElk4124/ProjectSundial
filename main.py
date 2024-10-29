import sys
import socket

import serial
from PyQt5 import QtWidgets, QtGui, QtCore

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

    def connect_to_pi(self):
        try:
            self.serial_connection = serial.Serial('/dev/cu.Bluetooth-Incoming-Port', 9600)
            self.log_message("Connected to Raspberry Pi")
            self.status_label.setText("Device Status: Connected")
        except serial.SerialException as e:
            self.log_message(f"Error connecting to Raspberry Pi: {e}")
            self.status_label.setText("Device Status: Error")

    def start_device(self):
        if self.serial_connection or True:
            # Read inputs from the input boxes
            try:
                total_ics = float(self.total_ics_input.text())
                gear_ratio = float(self.gear_ratio_input.text())
                steps_per_rotation = float(self.steps_per_rotation_input.text())
            except ValueError:
                self.log_message("Please enter valid numbers in all fields.")
                return

            if total_ics and gear_ratio and steps_per_rotation:
                # Create the command to send to the microcontroller
                command = f'start {total_ics} {gear_ratio} {steps_per_rotation}\n'

                self.log_message(f"Calculating IC: {steps_per_rotation * gear_ratio / total_ics}")
                # try:
                #     self.serial_connection.write(command.encode())  # Send the command
                #     self.status_label.setText("Device Status: Running")
                #     self.log_message(
                #         f"Device started with Total ICs: {total_ics}, Gear Ratio: {gear_ratio}, Steps/Rotation: {steps_per_rotation}")
                # except serial.SerialException as e:
                #     self.log_message(f"Error sending data to microcontroller: {e}")
            else:
                self.log_message("Please fill in all parameters before starting the device.")
        else:
            self.log_message("Not connected to the microcontroller! Please press Connect.")

    def stop_device(self):
        if self.serial_connection:
            try:
                self.serial_connection.write(b'stop\n')
                self.status_label.setText("Device Status: Stopped")
                self.log_message("Device stopped!")
            except serial.SerialException as e:
                self.log_message(f"Error stopping device: {e}")
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

