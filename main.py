import sys
import paramiko
from PyQt5 import QtWidgets, QtGui, QtCore


def get_input_value(input_field):
    """
    Helper method to retrieve a numeric value from a QLineEdit field.
    """
    try:
        value = input_field.text().strip()
        if not value:  # Check if the input is empty
            return None
        return float(value)
    except ValueError:
        return None


class DeviceControlApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.log_text = None
        self.ssh_client = None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Project Sundial Control Panel")
        self.setGeometry(100, 100, 1000, 700)

        main_layout = QtWidgets.QHBoxLayout()

        control_panel = QtWidgets.QVBoxLayout()

        # Status Label
        self.status_label = QtWidgets.QLabel("Device Status: Idle")
        self.status_label.setFont(QtGui.QFont("Arial", 18, QtGui.QFont.Bold))
        self.status_label.setAlignment(QtCore.Qt.AlignCenter)
        control_panel.addWidget(self.status_label)

        # Parameters Input Group
        parameters_group = QtWidgets.QGroupBox("Device Parameters")
        parameters_group.setStyleSheet(
            "QGroupBox { font-size: 16px; font-weight: bold; padding: 10px; border: 2px solid #008080; border-radius: 5px; }"
        )
        parameters_layout = QtWidgets.QFormLayout()
        self.total_ics_input = self.create_input_field("Total ICs", parameters_layout)
        self.gear_ratio_input = self.create_input_field("Gear Ratio", parameters_layout)
        self.steps_per_rotation_input = self.create_input_field("Steps per Rotation", parameters_layout)
        self.ip_address_input = self.create_input_field("Raspberry Pi IP Address", parameters_layout)
        parameters_group.setLayout(parameters_layout)
        control_panel.addWidget(parameters_group)

        # Buttons
        button_layout = QtWidgets.QVBoxLayout()
        button_layout.addWidget(self.create_button("Connect To Device", "#008080", self.connect_to_pi))  # Teal
        button_layout.addWidget(self.create_button("Step Forward", "#00BFFF", self.step_forward))  # Sky Blue
        button_layout.addWidget(self.create_button("Step Backward", "#00BFFF", self.step_backward))  # Sky Blue
        button_layout.addWidget(self.create_button("Test Connection", "#FFA500", self.test_connection))  # Light Orange
        button_layout.addWidget(self.create_button("Test First Device", "#FFA500", self.test_first_device))  # Light Orange
        button_layout.addWidget(self.create_button("Next Device", "#9370DB", self.next_device))  # Soft Purple
        button_layout.addWidget(self.create_button("Previous Device", "#9370DB", self.previous_device))  # Soft Purple
        button_layout.addWidget(self.create_button("Disconnect Pins", "#B22222", self.disconnect_pins))  # Deep Red
        button_layout.addWidget(self.create_button("Reconnect Pins", "#2E8B57", self.reconnect_pins))  # Emerald Green
        button_layout.addWidget(self.create_button("Disconnect From Device", "#B22222", self.disconnect_from_device))  # Deep Red
        control_panel.addLayout(button_layout)

        main_layout.addLayout(control_panel, 2)

        # Log Panel
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
                border: 2px solid #008080;
                border-radius: 25px;
                background-color: #f9f9f9;
            }
            QLineEdit:focus {
                border-color: #00BFFF;
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

    def log_message(self, message):
        self.log_text.append(message)

    def connect_to_pi(self):
        try:
            hostname = self.ip_address_input.text().strip()
            if not hostname:
                self.log_message("Please enter a valid IP address.")
                return

            username = "team6"
            password = "team6"

            self.ssh_client = paramiko.SSHClient()
            self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.ssh_client.connect(hostname, username=username, password=password)
            self.log_message(f"Connected to Raspberry Pi at {hostname} via SSH")
            self.status_label.setText("Device Status: Connected")
            self.execute_remote_command("connect_to_device")

            self.ssh_client.exec_command("sudo pigpiod")
        except Exception as e:
            self.log_message(f"Error connecting to Raspberry Pi: {e}")
            self.status_label.setText("Device Status: Error")

    def step_forward(self):
        self.execute_remote_command("step_forward")

    def step_backward(self):
        self.execute_remote_command("step_backward")

    def test_connection(self):
        self.execute_remote_command("Test_Connection")

    def test_first_device(self):
        self.execute_remote_command("test_first_device")

    def next_device(self):
        self.execute_remote_command("next_device")

    def previous_device(self):
        self.execute_remote_command("previous_device")

    def disconnect_pins(self):
        self.execute_remote_command("disconnect_pins")

    def reconnect_pins(self):
        self.execute_remote_command("reconnect_pins")

    def disconnect_from_device(self):
        if self.ssh_client:
            self.execute_remote_command("disconnect_from_device")
            self.ssh_client.close()
            self.log_message("Disconnected from Raspberry Pi")
            self.status_label.setText("Device Status: Disconnected")
        else:
            self.log_message("No active connection to disconnect.")

    def execute_remote_command(self, file_name):
        if not self.ssh_client or not self.ssh_client.get_transport().is_active():
            self.log_message("Not connected to Raspberry Pi. Please connect first.")
            return
        try:

            gear_ratio = get_input_value(self.gear_ratio_input)
            steps_per_rotation = get_input_value(self.steps_per_rotation_input)
            total_ics = get_input_value(self.total_ics_input)

            if gear_ratio is None or steps_per_rotation is None or total_ics is None:
                self.log_message("Please fill in all fields: Gear Ratio, Steps per Rotation, and Total ICs.")
                return

            if total_ics == 0:
                self.log_message("Total ICs cannot be zero.")
                return

            computed_value = (gear_ratio * steps_per_rotation) / total_ics
            command = f"python3 /home/team6/Desktop/stepper_testing/{file_name}.py {computed_value}"
            stdin, stdout, stderr = self.ssh_client.exec_command(command)
            output = stdout.read().decode()
            error = stderr.read().decode()

            if output:
                self.log_message(f"{computed_value} Output: {output}")
            if error:
                self.log_message(f"{computed_value} Error: {error}")
        except Exception as e:
            self.log_message(f"Error executing : {e}")


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = DeviceControlApp()
    window.show()
    window.showMaximized()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
