# livox-ros

ROS 2 workspace for Livox Mid-360: SDK, driver, and launch.

## Quick Start (Pixi)

```sh
git submodule update --init --recursive
pixi install
pixi run build
pixi run livox
```

Optional RViz:

```sh
pixi run ros2 launch livox_ros livox.launch.py rviz:=true
```

## Livox Setup

Set host IP to `192.168.10.50`. The LiDAR is at `192.168.10.130`.

Network settings live in `livox_ros/config/MID360_config.json`.

## Layout

| Path | Role |
|------|------|
| `Livox-SDK2/` | Livox SDK 2 (`livox_sdk2`) |
| `livox_ros_driver2/` | ROS 2 driver node |
| `livox_ros/` | `livox.launch.py`, Mid-360 config, RViz |

Humble is the default Pixi environment; use `pixi run -e jazzy` for Jazzy.
