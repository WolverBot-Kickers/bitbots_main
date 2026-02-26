# FRC Guide 3: The Superstructure (HCM)

In complex FRC robots, you often have a "Superstructure" class. This class manages the state of the *entire* robot to prevent illegal states.
*   "Don't shoot if the hood is down."
*   "Don't climb if the arm is extended."

In BitBots, this is the **Hardware Control Manager (HCM)** (`bitbots_hcm`).

## The Ultimate Gatekeeper
HCM sits between the "Behavior" (Brain) and the "Hardware" (Muscles).
*   **Code Location**: `src/bitbots_motion/bitbots_hcm`
*   **Logic**: Defined in `hcm.dsd`.

## The State Machine
HCM runs a Finite State Machine (FSM) that dictates what the robot is physically capable of doing right now.

### Key States (from `hcm.dsd`)
1.  **`START_UP`**: Robot is booting. Motors are turning on. Soft-start torque to prevent snapping gears.
2.  **`RUNNING`**: Normal operation.
    *   **`CONTROLLABLE`**: The "Behavior" is allowed to control the robot (Walk, Kick).
    *   **`FALLING`**: The IMU detected a fall. **Override everyone**.
        *   Action: `StopWalking`, `PlayAnimationFalling` (Protective tuck).
    *   **`FALLEN`**: Robot is on the ground.
        *   Action: Trigger `Dynup` to stand up.
    *   **`PENALTY`**: Robot is penalized by the ref.
        *   Action: Stand still, look down (optional), accept fate.
    *   **`HARDWARE_PROBLEM`**: Motor overheat or communication error.
        *   Action: Stop everything, maybe limp home or sit down.

## Why is it separate?
In FRC, you might put this in `RobotPeriodic`. We separate it so that **even if the Behavior code crashes**, the HCM (which is simple and robust) keeps running.
If the high-level strategy freezes, HCM will still detect a fall and protect the robot. It is the **Safety Layer**.

## Hierarchy of Control
1.  **Safety (HCM)**: Falling, Overheating. (Highest Priority)
2.  **Ref Game Controller**: Penalized, Game Over.
3.  **Autonomous Behavior**: Walking to ball, Kicking. (Lowest Priority)
