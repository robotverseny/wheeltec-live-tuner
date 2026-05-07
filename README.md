# Wheeltec Live Parameter Tuning Tool 🚀

This package provides a **Real-Time param tune GUI** for the Wheeltec Ackermann robots. It allows you to dynamically adjust the parameters of your basic navigation controllers (Follow The Gap and Simple Pursuit) without restarting ROS 2 nodes.

---

## 🛠 Features

*   **Real-time Tuning:** Adjust safety radii, velocity, and steering sensitivity on the fly.
*   **Dual Controller Support:** Dedicated controls for both `follow_the_gap` and `simple_pursuit`.
*   **ROS 2 Native:** Uses standard service calls (`SetParameters`) to communicate with active nodes.

---



## 🚀 Getting Started

### 1. Prerequisites
Ensure you have the following installed on your local machine or the robot:
*   **ROS 2** (Jazzy or Humble)
*   **PyQt6**
    ```bash
    sudo apt install python3-pip
    pip3 install PyQt6 --break-system-packages
    ```

### 2. Installation
Clone this package into your workspace's `src` folder:
```bash
cd ~/ros2_ws/src
# (Copy the package files here)
cd ~/ros2_ws
colcon build --packages-select live_parametisation
source install/setup.bash
```

### 3. Running the Tool
First, ensure your robot drivers and controllers are running (e.g., via `start_drivers`). Then, launch the tuning GUI:
```bash
ros2 run live_parametisation live_parametisation
```

---

## 🎮 Interface Overview

The GUI is split into two main sections:

### **Follow The Gap (FTG)**
*   **Safety Radius:** Adjust how far the robot stays from obstacles.
*   **Steering Sensitivity:** Fine-tune how aggressively the robot reacts to gaps.

### **Simple Pursuit (SP)**
*   **Velocity:** Change the target cruising speed.
*   **Angle Range:** Define the field of view (in degrees) for the pursuit logic.

---

## ⚙️ Technical Details

### **Topics & Services Used**
The tool acts as a client to the following ROS 2 parameter services:
*   `/follow_the_gap/set_parameters`
*   `/simple_pursuit/set_parameters`

### **Under the Hood**
The application runs the **ROS 2 Executor** in a background thread using `threading`, allowing the **PyQt6 Event Loop** to remain responsive while sending asynchronous service requests to the robot.

---

## 🔗 Useful Links
*   **Main Documentation:** [go.sze.hu/wh](https://go.sze.hu/wh)
*   **Robot Repo:** [JKK Research Center](https://github.com/jkk-research)

---
*Created by the Balazs*
```