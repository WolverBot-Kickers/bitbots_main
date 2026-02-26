# The FRC Student's Guide to the BitBots Codebase

Welcome to the team! If you're coming from FIRST Robotics (FRC), this codebase matches many concepts you already know, just with different names. We use **ROS 2** (Robot Operating System) instead of WPILib, but the logic is surprisingly similar.

Think of our robot, **Wolfgang**, as a highly advanced FRC robot with a lot of degrees of freedom (20 motors instead of just 4-6 for a drivetrain!).

## 1. The "Robot.java" (System Composition)

In FRC, you have `Robot.java` or `RobotContainer.java` where you instantiate all your subsystems and commands.

In our ROS 2 world, we use **Launch Files** to do this. The main entry point is in **`bitbots_misc/bitbots_bringup`**.

*   **`teamplayer.launch`**: This is like your `robotInit()`. It starts everything needed for a match:
    *   **Hardware Interface** (reading sensors, writing motors).
    *   **Motion Control** (Walking, Kicking).
    *   **Behavior** (Decision making / Autonomous).
    *   **Vision** (Seeing the ball).

## 2. Subsystems (The Hardware Abstraction)

You are used to `SubsystemBase` classes like `DriveSubsystem`, `ShooterSubsystem`, etc. Here is how they map:

### The Drivetrain -> `bitbots_motion`
Instead of a differential drive or swerve drive, we have a **Walking Engine**.
*   **`bitbots_quintic_walk`**: This is our Swerve Drive. It takes `Encoders` (joint positions) and `IMU (Gyro)` data and calculates how to move the legs to walk in a direction (x, y, theta).
*   **`bitbots_head_mover`**: Think of this as a **Turret Subsystem**. It points the camera (head) towards the ball or goal.

### The Superstructure -> `bitbots_hcm`
In advanced FRC robots, you often have a "Superstructure" or "RobotState" machine that prevents the robot from doing illegal actions (like extending the elevator while the arm is down).
*   **`bitbots_hcm` (Hardware Control Manager)**: This is our Superstructure. It is the ultimate gatekeeper.
    *   **State Machine**: It tracks if the robot is `WALKING`, `FALLING`, `GETTING_UP`, or `PENALIZED`.
    *   **Protection**: If the robot falls, HCM takes over and runs the "Get Up" routine (like a self-righting climber). It stops the walking engine from trying to walk while lying on the ground.

### The "Limelight" -> `bitbots_vision`
We don't use a Limelight, but the concept is identical.
*   **`bitbots_vision`**: This runs on the robot's main computer (like detailed processing on a Coprocessor or Jetson).
    *   **Input**: Raw images from the camera.
    *   **Output**: Coordinates of the Ball, Goal Posts, and Obstacles.
    *   It publishes these "targets" to ROS topics (similar to putting values into NetworkTables).

## 3. Command-Based Programming (Behavior)

In FRC, you schedule `Commands` (e.g., `DriveToNote`, `ShootWhileMoving`).

We use **`bitbots_behavior`** with a library called **`dynamic_stack_decider` (DSD)**.
*   **DSD** is like a fancy **CommandGroup**. instead of a simple sequence, it's a **Decision Tree**.
*   **Decisions** (Conditionals): "Do I see the ball?", "Am I close enough to kick?"
*   **Actions** (Commands): "Walk to Ball", "Kick", "Search for Ball".
*   **`bitbots_body_behavior`**: This is the main "Autonomous" logic for playing soccer. It runs continuously (even in Teleop, technically, as the robot plays autonomously).

## 4. Hardware Interface (HAL) -> `bitbots_lowlevel`

In FRC, WPILib handles the CAN bus and Motor Controllers (TalonFX, SparkMax).
*   **`bitbots_ros_control`**: This is our HAL. It talks to the **Dynamixel Servos** (our motors) using a protocol called Dynamixel SDK (similar to CAN).
*   It reads positions/velocities/currents and writes goal positions.

## 5. Simulation -> `bitbots_simulation`

Just like FRC Sim (SimGUI), we have a full physics simulator.
*   **Webots**: Our simulator of choice. It simulates gravity, friction, and collisions.
*   We can run the *exact same code* on the simulator as on the real robot.
*   **`bitbots_webots_sim`**: Bridges the simulator to our ROS system.

## Summary Table

| FRC Concept | BitBots Package | Description |
| :--- | :--- | :--- |
| **RobotContainer** | `bitbots_bringup` | Starts all subsystems/commands. |
| **Drivetrain** | `bitbots_quintic_walk` | Handles walking kinematics. |
| **Turret** | `bitbots_head_mover` | Points the camera. |
| **Superstructure** | `bitbots_hcm` | Manages robot state (falling/standing). |
| **Autonomous** | `bitbots_body_behavior` | Main game logic/decisions. |
| **Limelight** | `bitbots_vision` | Object detection (Ball/Goal). |
| **Pigeon/NavX** | `bitbots_imu` | Gyroscope handling. |
| **Sim GUI** | `bitbots_simulation` | Webots physics sim. |

## Quick Start (Where to Look)

*   **Want to change how we play?** Go to `bitbots_behavior/bitbots_body_behavior/actions` or `decisions`.
*   **Want to change how we walk?** Go to `bitbots_motion/bitbots_quintic_walk`.
*   **Want to fix a camera issue?** Go to `bitbots_vision`.
*   **Robot falling too much?** Check `bitbots_hcm`.
