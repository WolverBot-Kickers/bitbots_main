# FRC Guide 5: Autonomous Behavior (Command-Based)

In FRC, you write `Commands` and `CommandGroups`.
Reference: `src/bitbots_behavior/bitbots_body_behavior/behavior_dsd/main.dsd`

## Dynamic Stack Decider (DSD)
We use DSD, which is a **Behavior Tree** meant for soccer. It replaces `SequentialCommandGroup` with something smarter.

### Structure
1.  **Decisions ($)**: Questions. Equivalent to `Trigger` or `if/else`.
    *   Examples: `$BallSeen`, `$IsPenalized`, `$KickOffTimeUp`.
2.  **Actions (@)**: Commands. Equivalent to `InstantCommand` or `RunCommand`.
    *   Examples: `@GoToBall`, `@Kick`, `@Stand`, `@SearchBall`.

### The "Auto Routine"
Our "Auto" is actually our "Teleop". The robot plays autonomously *all the time*.
The root of the tree (`main.dsd`) decides the high-level strategy.

#### Example: The `NormalBehavior` Stack
```text
#NormalBehavior
$BallSeen
    NO --> #SearchBall                <-- CommandGroup: Look around, spin
    YES --> $KickOffTimeUp
        YES --> $ConfigRole
            GOALIE --> #GoalieRole    <-- CommandGroup: Guard net
            ELSE --> #StrikerRole     <-- CommandGroup: Attack
```
*   **Logic**: "Do I see the ball? If No, Search. If Yes, check my role. If Striker, Attack."

### Parameters
Just like passing values to a Command constructor.
*   `@GoToBall + distance:0.5`
    *   Go to the ball, but stop 0.5 meters away.

### Blackboard (The "RobotState")
How do Decisions know if the ball is seen?
They read from the **Blackboard**. This is a shared memory object (Singleton) where Vision writers write `ball_seen = true` and Decisions read it.
This is similar to having a static `RobotState` class in FRC that all commands can access.

## Strategy Changes
To change strategy, you edit `.dsd` files. You don't need to recompile C++ code usually, as DSD is interpreted at runtime!
