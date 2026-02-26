# FRC Guide 4: Vision (The "Limelight")

In FRC, you usually treat Vision as a black box (Limelight). You tune a pipeline, and it gives you `tx`, `ty`, and `ta`.
In BitBots, we build the Limelight software ourselves.

## The Pipeline (`bitbots_vision`)
Just like a Limelight pipeline, processed images go through stages.
**File**: `config/visionparams.yaml`

1.  **Input**: Raw image from the camera (`/camera/image_proc`).
2.  **Detection (Neural Network)**:
    *   We uses a custom YOLO-based model called **YOEO (You Only Encode Once)**.
    *   It identifies: `Ball`, `GoalPost`, `Robot`, `Line`.
    *   **Tunables**:
        *   `yoeo_conf_threshold`: Confidence threshold (like `Minimum Area` or `Confidence`).
        *   `yoeo_nms_threshold`: Non-Maximum Suppression (prevents seeing double balls).
3.  **Projection (3D Math)**:
    *   Limelight gives you angles (`tx`, `ty`). We need meters (X, Y).
    *   We use the **Camera Matrix** and the **Robot Kinematics** (Head tilt + Body height) to project the pixel onto the ground plane.
    *   Result: "Ball is at (2.5m, -0.5m) relative to the robot."

## Output Topics (NetworkTables)
*   **`/balls_in_image`**: Unfiltered list of ball candidates.
*   **`/ball_position_relative`**: The final 3D position of the ball (X, Y, Z).

## Debugging (The Stream)
*   Enable `component_debug_image_active: true` in `visionparams.yaml`.
*   This publishes an image with bounding boxes drawn on it, just like the Limelight web interface.
*   You view it in **RQT** (The ROS equivalent of Shuffleboard).
