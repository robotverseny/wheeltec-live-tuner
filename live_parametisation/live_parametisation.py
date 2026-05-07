import sys
import threading
import rclpy
from rclpy.node import Node
from rcl_interfaces.srv import SetParameters
from rcl_interfaces.msg import Parameter, ParameterValue, ParameterType
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QDoubleSpinBox, QGroupBox, QPushButton, QFrame)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

STYLESHEET = """
    QWidget {
        background-color: #121212;
        color: #E0E0E0;
        font-family: 'Segoe UI', sans-serif;
    }
    QGroupBox {
        border: 2px solid #333333;
        border-radius: 10px;
        margin-top: 20px;
        font-weight: bold;
        font-size: 14px;
        color: #00ADB5;
    }
    QGroupBox::title {
        subcontrol-origin: margin;
        left: 10px;
        padding: 0 5px 0 5px;
    }
    QLabel {
        font-size: 12px;
        color: #B0B0B0;
    }
    QDoubleSpinBox {
        background-color: #1E1E1E;
        border: 1px solid #444444;
        border-radius: 5px;
        padding: 5px;
        min-width: 80px;
    }
    QPushButton {
        background-color: #00ADB5;
        color: #EEEEEE;
        border-radius: 5px;
        padding: 10px;
        font-weight: bold;
        margin-top: 10px;
    }
    QPushButton:hover {
        background-color: #00CFD5;
    }
    QPushButton:pressed {
        background-color: #007D82;
    }
"""

class RemoteControlNode(Node):
    def __init__(self):
        super().__init__('remote_param_controller')
        self.ftg_client = self.create_client(SetParameters, '/follow_the_gap/set_parameters')
        self.sp_client = self.create_client(SetParameters, '/simple_pursuit/set_parameters')

    def send_params(self, node_type, params_dict):
        client = self.ftg_client if node_type == "FTG" else self.sp_client
        
        if not client.wait_for_service(timeout_sec=1.0):
            self.get_logger().error(f'Service not available: {client.srv_name}')
            return

        request = SetParameters.Request()
        for name, value in params_dict.items():
            param = Parameter()
            param.name = name
            val = ParameterValue()
            
            if isinstance(value, int):
                val.type = ParameterType.PARAMETER_INTEGER
                val.integer_value = value
            else:
                val.type = ParameterType.PARAMETER_DOUBLE
                val.double_value = float(value)
            
            param.value = val
            request.parameters.append(param)

        client.call_async(request)
        self.get_logger().info(f'Params sent to: {node_type}')

class ControlGui(QWidget):
    def __init__(self, node):
        super().__init__()
        self.node = node
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Wheeltec Mission Control')
        self.setMinimumWidth(400)
        self.setStyleSheet(STYLESHEET)
        
        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)

        header = QLabel("ROBOT PARAMETERS")
        header.setFont(QFont('Segoe UI', 18, QFont.Weight.Bold))
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(header)

        ftg_group = QGroupBox("FOLLOW THE GAP")
        ftg_layout = QVBoxLayout()
        self.ftg_radius = self.create_input_row("Safety Radius", 2.0, ftg_layout)
        self.ftg_sens = self.create_input_row("Steering Sensitivity", 0.7, ftg_layout)
        btn_ftg = QPushButton("APPLY FTG CONFIG")
        btn_ftg.clicked.connect(self.apply_ftg)
        ftg_layout.addWidget(btn_ftg)
        ftg_group.setLayout(ftg_layout)
        main_layout.addWidget(ftg_group)

        sp_group = QGroupBox("SIMPLE PURSUIT")
        sp_layout = QVBoxLayout()
        self.sp_vel = self.create_input_row("Velocity", 1.0, sp_layout)
        self.sp_range = self.create_input_row("Angle Range", 360, sp_layout, is_int=True)
        btn_sp = QPushButton("APPLY PURSUIT CONFIG")
        btn_sp.clicked.connect(self.apply_sp)
        sp_layout.addWidget(btn_sp)
        sp_group.setLayout(sp_layout)
        main_layout.addWidget(sp_group)

        self.setLayout(main_layout)

    def create_input_row(self, label_text, default, layout, is_int=False):
        row_widget = QWidget()
        row_layout = QHBoxLayout(row_widget)
        row_layout.setContentsMargins(0, 5, 0, 5)
        
        lbl = QLabel(label_text)
        spin = QDoubleSpinBox()
        
        if is_int:
            spin.setDecimals(0)
            spin.setRange(0, 360)
        else:
            spin.setRange(0.0, 10.0)
            spin.setSingleStep(0.1)
            
        spin.setValue(float(default))
        
        row_layout.addWidget(lbl)
        row_layout.addStretch()
        row_layout.addWidget(spin)
        layout.addWidget(row_widget)
        return spin

    def apply_ftg(self):
        params = {
            "safety_radius": self.ftg_radius.value(), # float
            "steering_sensitivity": self.ftg_sens.value() # float
        }
        self.node.send_params("FTG", params)

    def apply_sp(self):
        params = {
            "velocity": self.sp_vel.value(), # float
            "angle_range": int(self.sp_range.value()) # int
        }
        self.node.send_params("SP", params)

def main():
    rclpy.init()
    node = RemoteControlNode()
    
    thread = threading.Thread(target=rclpy.spin, args=(node,), daemon=True)
    thread.start()

    app = QApplication(sys.argv)
    gui = ControlGui(node)
    gui.show()
    
    sys.exit(app.exec())

if __name__ == '__main__':
    main()