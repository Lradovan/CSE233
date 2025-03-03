## **Autoware CARLA Bridge Installation Guide**

This is a guide for installing an interface between CARLA and Autoware. The interface used is [here](https://autowarefoundation.github.io/autoware.universe/main/simulator/autoware_carla_interface/). It requires Ubuntu 22.04. Do not attempt to install on WSL2, as you will likely run into performance issues. I also recommend having a GPU with more than 8GB vram, preferably 12 or 16. Running CARLA and Autoware simultaneously is difficult. Here are four main steps:

1. Installing ROS2
2. Building Autoware from Source
3. Installing CARLA
4. Downloading the maps

### **Installing ROS2 Humble**

1. Follow the instructions [here](https://docs.ros.org/en/humble/Installation/Ubuntu-Install-Debs.html) to install ROS2 Humble.

### **Building Autoware**

The official package for communication between Autoware and CARLA is integrated into Autoware Universe, which is an extension of Autoware Core. To make use of the bridge, we can build Autoware from source.

1. Follow the instructions here to build from source [here](https://autowarefoundation.github.io/autoware-documentation/main/installation/autoware/source-installation/). Do **not** overlook step 5. It is crucial to get the bridge properly working. Follow the recommendations for enabling multicast as well as saving a CycloneDDS configuration. In addition, you may find it necessary to set `export ROS_DOMAIN_ID=3` after making these network changes.

2. Autoware has an in-depth page [here](https://autowarefoundation.github.io/autoware-documentation/main/support/troubleshooting/#build-issues) covering many tips for fixing build issues. I found a 16GB swap file to be necessary when installing, as well as limiting the job number while building by specifying `MAKEFLAGS="-j4"`. Depending on the number of CPU cores and memory in your PC, these steps may not be necessary.

3. For issues related to NVIDIA drivers, I found [this](https://github.com/orgs/autowarefoundation/discussions/4642) discussion to be very helpful. There are instructions to clear existing drivers, and how to properly install TensorRT and CUDA.

4. If you run into ccache environment variable issues, I found the solution [here](https://github.com/autowarefoundation/autoware/issues/4605).

5. For errors related to CMAKE, try to do a clean build and be sure to run `rosdep update` and `rosdep install` to find the necessary dependencies.

### **Testing Autoware**

Once Autoware has finishing building sucessfully (stderr warnings can be ignored), I think it is a good idea to test it independent of CARLA. [Here](https://autowarefoundation.github.io/autoware-documentation/main/tutorials/ad-hoc-simulation/planning-simulation/) is a simple tutorial that can be followed. This tutorial should also help with understanding how to interact with GUI (it will look a little different, but all the buttons are the same).

### **Installing CARLA**

If Autoware is working on its own, the last major step is to install CARLA version 0.9.15.

1. Install version 0.9.15 of CARLA. [Here](https://github.com/carla-simulator/carla/releases/tag/0.9.15/) is the release page.

2. Install CARLA's Python API: `python -m pip install carla==0.9.15`

### **Download the Maps**

Autoware needs access to special maps in order to work with CARLA.

1. Download the map data from [here](https://bitbucket.org/carla-simulator/autoware-contents/src/master/maps/). Follow the instructions from the interface [repo](https://autowarefoundation.github.io/autoware.universe/main/simulator/autoware_carla_interface/) and give the files the proper naming convention. Without the proper structure here, Autoware will not be able to load the maps.

### **Run Autoware and CARLA** (adpated from [here](https://autowarefoundation.github.io/autoware.universe/main/simulator/autoware_carla_interface/#install))

1. Run CARLA: 
`./CarlaUE4.sh -prefernvidia -quality-level=Low`

2. Run Autoware ros nodes: `ros2 launch autoware_launch e2e_simulator.launch.xml map_path:=$HOME/autoware_map/Town01 vehicle_model:=sample_vehicle sensor_model:=awsim_sensor_kit simulator_type:=carla carla_map:=Town01`

3. Wait for Autoware to initialize a pose. This might take a few seconds. By default, Autoware will initialize the ego at the edge of the map, but then correct itself to the true position. In CARLA, you can navigate to the location of the ego to confirm that it has been correctly initialized.

4. Set a goal position by selecting the "2D Goal Pose" button and placing a green arrow.

5. Wait for the planning to complete. There should be a green path from the ego to the destination, with blue lines along the edges of the lane. 

6. Click the "auto" button in the GUI to engage the vehicle. Alternatively, you can do so manually from the CLI with: `source ~/autoware/install/setup.bash` and `ros2 service call /api/operation_mode/change_to_autonomous autoware_adapi_v1_msgs/srv/ChangeOperationMode {}`

7. The vehicle should navigate to the goal pose and then change to a stopped mode. At this point, you can change the location of the vehicle using "2D Pose Estimate," or set a new route.

### **Current Issues**

I currently experience a number of issues, which are likely just related to my limited hardware.

1. Volatile frame rate. Sometimes I get a relatively smooth 30 FPS inside of both Autoware and CARLA, and other times I might get 5-10 FPS. 

2. Sometimes there is no camera output inside of Autoware. Restarting usually fixes this.

3. Sometimes setting the location of the ego vehicle causes CARLA to crash.