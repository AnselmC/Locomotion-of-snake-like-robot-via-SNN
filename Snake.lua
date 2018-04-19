-- This ACM-R5 model demonstrates distributed control, where each body segment is controlled by its own script
-- This is meant as an example only. Have a look at the control method of the "ant hexapod", that is much simpler.

function setTurningRadius_cb(msg)
    -- Turning Radius subscriber callback
    radius = msg.data
    b = 0
    if (radius >= 1 or radius <= -1) then
        b = l / (K*radius) 
    end
    --print(radius)
end

function resetRobot_cb(msg)
    -- Reset robot subscriber callback
    print("Reset robot")
    allModelObjects=simGetObjectsInTree(robotHandle) -- get all objects in the model
    simSetThreadAutomaticSwitch(false)
    for i=1,#allModelObjects,1 do
        simResetDynamicObject(allModelObjects[i]) -- reset all objects in the model
    end
    t = 0
    for i=1,K,1 do
        simSetJointPosition(joints_v[i], 0)
        simSetJointTargetPosition(joints_v[i], 0)
    end
    simSetObjectPosition(robotHandle,-1,init_pos)
    simSetObjectOrientation(robotHandle,-1,init_ori)
    simSetThreadAutomaticSwitch(true)
end

if (sim_call_type==sim_childscriptcall_initialization) then
    robotHandle=simGetObjectAssociatedWithScript(sim_handle_self)
    
    init_pos = simGetObjectPosition(robotHandle, -1)
    init_ori = simGetObjectOrientation(robotHandle, -1)

    joints_v={-1,-1,-1,-1,-1,-1,-1,-1}
    for i=1,8,1 do
        joints_v[i]=simGetObjectHandle('Snake_vJoint_'..(i))
    end


    -- Check if the required ROS plugin is there:
    moduleName=0
    moduleVersion=0
    index=0
    pluginNotFound=true
    while moduleName do
        moduleName,moduleVersion=simGetModuleName(index)
        if (moduleName=='RosInterface') then
            pluginNotFound=false
        end
        index=index+1
    end

    -- Prepare Camera handle
    cameraHandle=simGetObjectHandle('DVS_128')
    showCameraView=simGetScriptSimulationParameter(sim_handle_self,'showCameraView')
    print(showCameraView)
    if (showCameraView) then
        print("Camera view activated")
        floatingView=simFloatingViewAdd(0.2,0.8,0.4,0.4,0)
        simAdjustView(floatingView,cameraHandle,64)
    end

    if (not pluginNotFound) then
                -- Prepare the sensor publisher and the motor speed subscribers:
        turnRadiusSub=simExtRosInterface_subscribe('/turningRadius','std_msgs/Float32','setTurningRadius_cb')
        resetRobotSub=simExtRosInterface_subscribe('/resetRobot','std_msgs/Bool','resetRobot_cb')
    end

    t=0
    step=0
    K = 8
    local m = 0.18
    -- linear reduction parameters (set y = 0 and z = 1 for disabling)
    y = 0.5
    z = 1 - y
    -- set of control Parameters:
    -- frequency
    w = 0.5*math.pi
    -- amplitude
    a = 40*math.pi/180
    -- wavelength
    lambda = 4000*math.pi/180
    p = -1

    
    local theta = {0,-1,-1,-1,-1,-1,-1,-1,-1}
    local head_dir = 0
    for i=1,K,1 do
        amp = a* ((i-1)*y/K + z)
        theta[i+1] = theta[i] + amp * math.cos(lambda * (i-1))
        head_dir = head_dir + theta[i+1]
    end

    head_dir = head_dir/(K+1)

    l = 0;
    for i=1,K+1,1 do
        l = l + math.cos(theta[i] - head_dir)
    end
    l = m * l;

    b = 0
end 

if (sim_call_type==sim_childscriptcall_cleanup) then 
    if not pluginNotFound then
        -- Following not really needed in a simulation script (i.e. automatically shut down at simulation end):
        simExtRosInterface_shutdownSubscriber(turnRadiusSub)
        simExtRosInterface_shutdownSubscriber(resetRobotSub)
    end
    if auxConsole then
        simAuxiliaryConsoleClose(auxConsole)
    end
end


if (sim_call_type==sim_childscriptcall_actuation) then
    t=t+simGetSimulationTimeStep()
    step=step+1
    
    
    local theta = 0
    local head_dir = theta

    for i=2,K,1 do
        amp = a* ((i-1)*y/K + z)
        phi = b + amp*math.cos(w*t - lambda * (i-1))
        simSetJointTargetPosition(joints_v[i], -phi*(1-math.exp(p*t)))

        phi = simGetJointPosition(joints_v[i])
        theta = theta + phi
        head_dir = head_dir + theta
    end
    head_dir = head_dir/(K+1)
    
    -- Print parameters every 10 steps
    if(math.fmod(step,10)==0) then
        print("---------",step,"--------")
        print("Radius:\t", radius)
        print("b:\t", b)
        print("Amplitude:", amp)
        print("Phi:\t", phi)
        print("Theta:\t", theta)
        print("Head dir:", head_dir)
        print("--------------------------------")
    end

    -- Head Compensation
    simSetJointTargetPosition(joints_v[1], -head_dir*(1-math.exp(p*t)))

end 
