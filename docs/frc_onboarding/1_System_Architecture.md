# FRC Guide 1: System Architecture & "Robot.java"

In FRC, your code starts at `Main.java`, which launches `Robot.java`, which initializes `RobotContainer.java`.
In ROS 2 (BitBots), we don't have a single "Monolithic" program. Instead, we have many small programs ("Nodes") that talk to each other.

### The "Deploy Code" Equivalent
In FRC, you run `./gradlew deploy`.
Here, we use **colcon build** to compile and a **Launch File** to start.

### The "RobotContainer"
The file that ties everything together is `bitbots_bringup/launch/teamplayer.launch`.
*   **What it does**:
    1.  Starts the **Hardware Interface** (Motor Drivers).
    2.  Starts the **Motion Engine** (Walking).
    3.  Starts the **Behavior** (Strategy).
    4.  Starts **Vision** (Camera processing).
    
    If you want to "comment out a subsystem" (e.g., test walking without vision), you would comment out the `<include file="..." />` line in this launch file.

### Inter-Process Communication (NetworkTables on Steroids)
In FRC, you use `NetworkTables` to send data between the Rio and distinct places like the Driver Station or a Coprocessor.
In ROS 2, **Everything is NetworkTables**.
*   **Topics**: Named channels of data (e.g., `/ball_position`, `/joint_states`).
*   **Publishers**: Writers (e.g., Vision publishes ball position).
*   **Subscribers**: Readers (e.g., Behavior reads ball position).
*   **Messages**: The data structure (e.g., `Vector3`, `Image`, `JointState`).

### Directory Structure Map
| FRC Concept | BitBots Location |
| :--- | :--- |
| **src/main/java** | `src/` (Root of all code) |
| **com.team254.subsystems** | `bitbots_motion`, `bitbots_vision` |
| **com.team254.commands** | `bitbots_body_behavior` |
| **vendor_deps** | `bitbots_msgs`, `pylint` (managed by `package.xml`) |
| **build.gradle** | `CMakeLists.txt` & `package.xml` |

### Key Takeaway
Wolfgang is not one program. It is a **Team of Programs**.
*   The **Motion Program** focuses solely on keeping balance.
*   The **Vision Program** focuses solely on finding the ball.
*   The **Behavior Program** decides *what* to do based on the other two.

This makes debugging easier: If the robot falls, you check the **Motion** logs. If it walks into a wall, you check **Vision**. If it sees the ball but stands still, you check **Behavior**.
