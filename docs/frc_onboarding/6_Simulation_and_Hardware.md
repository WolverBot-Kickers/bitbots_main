# FRC Guide 6: Simulation & Hardware

## Simulation (Webots)
In FRC, you use the Glass/SimGUI to test logic.
We use **Webots**.
*   **Physics**: It simulates mass, gravity, friction, and motor torque.
*   **Bridge**: `bitbots_webots_sim` acts as the "Hardware Abstraction Layer" for the sim.
    *   It takes ROS commands (`JointPositions`) and sends them to Webots.
    *   It reads Webots sensors (Camera, IMU) and publishes ROS topics.
*   **Benefit**: The Behavior and Motion code **does not know** it is in a simulation. It talks to the exact same topics.

## Hardware Interface (ROS Control)
On the real robot, we don't use `CANSparkMax` or `TalonFX` classes directly in our logic.
We use **ROS Control**.

### The "HAL"
*   **Package**: `bitbots_ros_control`
*   **Dynamixel SDK**: We use Dynamixel servos (smart servos with internal PIDs).
*   **The Loop**:
    1.  **Read**: Get current Angle, Velocity, Load from all 20 motors via USB-to-TTL.
    2.  **Update**: Run the Controller Manager (Motion code runs here).
    3.  **Write**: Send new Goal Position to motors.

### `ros2_control` Tags
In the URDF (Robot Description), we define "Joints".
```xml
<ros2_control name="WebotsControl" type="system">
  <joint name="HeadPan">
    <command_interface name="position"/>
    <state_interface name="position"/>
  </joint>
</ros2_control>
```
reference: `bitbots_webots_sim/protos/robots/Wolfgang/Wolfgang.proto` (conceptually similar).

This tells the system: "There is a motor called HeadPan. You can tell it where to go (command position) and ask where it is (state position)."

## Summary
*   **Sim**: Webots sends fake sensor data, accepts motor commands.
*   **Real**: `bitbots_ros_control` sends real sensor data, accepts motor commands.
*   **The Code**: Doesn't care which one is running!
