# FRC Guide 2: Motion Control (The Subsystems)

## 1. The Drivetrain: `bitbots_quintic_walk`
Wolfgang doesn't have wheels. His "Drivetrain" is a **Walking Engine**.
*   **Type**: Omnidirectional (Swerve-like). He can move X, Y, and Rotate (Theta).
*   **Control Loop**: Open-loop gait generation with Closed-loop stabilization (IMU Feedback).
    *   **Inputs**: `cmd_vel` (Twist message: x speed, y speed, turn speed).
    *   **Outputs**: `JointPositions` (Angle for each motor).

### Tunables (PID & Kinematics)
In `walking_wolfgang_robot.yaml`, you find the "Swerve Module Constants":
*   `freq`: Step frequency (How fast he steps).
*   `double_support_ratio`: How long both feet are on the ground (Stability vs. Speed).
*   `foot_rise`: How high he lifts his feet (Clearance).
*   **Stabilization**:
    *   `imu_active`: Like using a Pigeon IMU to correct driving straight.
    *   `trunk_pitch`: Leaning forward/back to stay balanced.

## 2. The Turret: `bitbots_head_mover`
Usually, the camera is on a pan-tilt mechanism (the Neck). This is effectively a **Turret**.
*   **Goal**: Keep the camera pointed at the "Target" (Ball or Goal).
*   **Modes**:
    *   `Search`: Scan the field in a pattern.
    *   `Track`: Lock onto the ball (PID control loop on the neck motors).
    *   `LookAt`: Point to a specific 3D coordinate.

## 3. The Special Actions: `bitbots_dynup` & `bitbots_dynamic_kick`
*   **Dynup**: This is like a **Climber** or **Self-Righting Mechanism**.
    *   If the robot falls, Dynup calculates a trajectory to push itself back up.
    *   It handles "Front Standup" and "Back Standup".
*   **Dynamic Kick**: This is the **Shooter**.
    *   Unlike a flywheel, it swings the leg.
    *   It calculates inverse kinematics to hit the ball at a specific velocity vector.
    *   **Tunables**: `kick_vel`, `kick_rise_factor`.

## FRC Analogy Summary
| BitBots Component | FRC Equvalent | Note |
| :--- | :--- | :--- |
| `quintic_walk` | **SwerveDriveSubsystem** | Holonomic control (X, Y, Theta). |
| `head_mover` | **TurretSubsystem** | Points the sensor/effector. |
| `dynup` | **ClimberSubsystem** | Pre-programmed heavy sequence. |
| `dynamic_kick` | **ShooterSubsystem** | Aim and fire logic. |
