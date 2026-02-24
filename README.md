# NTU OneArena 2024 Robotic Maze

Autonomous maze-solving stack for the NTU OneArena robotics competition (Sep 2023 to Jun 2024), combining:

- DJI RoboMaster Python control scripts for marker-based navigation and object handling
- Arduino firmware for IR-triggered motorized door control
- Supporting maze sketches and route plans

OneArena is a team-based workshop and competition introducing pre-university students in Singapore to robotics and coding through interdisciplinary problem-solving.

## Project Highlights

- Visual-marker-guided autonomous navigation with PID-based alignment
- Competition route logic for both easy and hard maze layouts
- Object pickup/drop flow integrated with RoboMaster robotic arm + gripper
- Custom door mechanism controlled by Arduino (IR + ultrasonic + dual motors)

## Repository Structure

```text
.
|-- Arduino/
|   |-- Version 2 (Current Version)/
|   |   |-- DoorBlackType1 Code/BlackType1.ino
|   |   |-- DoorWhiteType1 Code/WhiteType1.ino
|   |   |-- Independent Programs for Testing/
|   |   |   |-- IRControl/IRControl.ino
|   |   |   |-- USControl/USControl.ino
|   |   |   |-- MotorControl/MotorControl.ino
|   |   |   `-- CompleteCodeDraft/CompleteCodeDraft.ino
|   |   |-- Circuit Design.png
|   |   `-- Diagram.png
|   `-- Custom_UI.dsp.bin
|-- Maze Function/
|   |-- 2024_Base_Template.py
|   |-- Comp_2024_Route_Easy.py
|   |-- Comp_2024_Route_Hard.py
|   |-- 2024_Route_Easy.dsp
|   `-- 2024_Route_Hard.dsp
`-- Sketch/
    |-- Easy.jpg
    |-- Hard.jpg
    `-- Combined.jpg
```

## Autonomous Navigation (RoboMaster Python)

Main route scripts:

- `Maze Function/Comp_2024_Route_Easy.py`
- `Maze Function/Comp_2024_Route_Hard.py`

Core behaviors in these scripts:

- Marker-seeking and centering using PID (`PIDCtrl`)
- State transitions for `pickup`, `drop`, turning, and obstacle/door handling
- Motion control wrappers (`move`, `turn`, `displace`)
- Per-marker route commands (e.g., S-course, U-turn, push, wait/door logic)

These files are intended to run in DJI RoboMaster's Python runtime environment, where APIs such as `chassis_ctrl`, `vision_ctrl`, `robotic_arm_ctrl`, `gripper_ctrl`, and `rm_define` are available.

## Arduino Door Controller

Primary firmware:

- `Arduino/Version 2 (Current Version)/DoorWhiteType1 Code/WhiteType1.ino`
- `Arduino/Version 2 (Current Version)/DoorBlackType1 Code/BlackType1.ino`

Both use:

- `IRremote` for trigger detection
- `NewPing` for ultrasonic distance-based motor stopping profiles
- H-bridge motor control pins (`enA/enB`, `in1..in4`)

### Arduino Dependencies

Install via Arduino Library Manager:

- `IRremote`
- `NewPing`

## Getting Started

### 1. Clone

```bash
git clone https://github.com/NeoHwang98/DJI-NTU-OneArena2024
cd "NTU OneArena 2024 Robotic Maze"
```

### 2. Run/Deploy RoboMaster Route Script

1. Open RoboMaster script environment.
2. Load one of:
   - `Maze Function/Comp_2024_Route_Easy.py`
   - `Maze Function/Comp_2024_Route_Hard.py`
3. Calibrate marker IDs, PID gains, and movement thresholds for your field setup.

### 3. Upload Arduino Firmware

1. Open desired `.ino` in Arduino IDE.
2. Select board/port.
3. Install required libraries (`IRremote`, `NewPing`).
4. Upload and validate behavior using serial monitor.

## Notes and Calibration

- Marker IDs and behavior mapping are embedded in `corefunc(...)` within each route script.
- Distance thresholds in pickup/drop/door logic are hardware-specific and should be re-tuned after mechanical changes.
- `BlackType1.ino` currently includes an extra empty `setup()`/`loop()` block at the end; clean this before production upload.
