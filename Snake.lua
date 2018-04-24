function setTurningRadius_cb(msg)
    -- Turning Radius subscriber callback
    radius = msg.data
    b = 0

    if (radius >= 1 or radius <= -1) then
        b = l / (K*radius) 
    end
end

function resetRobot_cb(msg)
    -- Reset robot subscriber callback
    print("--------------------------------")
    print("----------Reset Snake-----------")
    print("--------------------------------")

     -- get all objects in the model
    allModelObjects=simGetObjectsInTree(robotHandle) 
    simSetThreadAutomaticSwitch(false)
  
    -- reset all objects in the model
    for i=1,#allModelObjects,1 do
        simResetDynamicObject(allModelObjects[i])
    end

    for i=1,K,1 do
        simSetJointPosition(joints_v[i], 0)
        simSetJointTargetPosition(joints_v[i], 0)
    end

    simSetObjectPosition(robotHandle,-1,init_pos)
    for i=1,#init_pos,1 do
        print("init_pos["..(i).."]:", init_pos[i])
    end

    simSetObjectOrientation(robotHandle,-1,init_ori)
    for i=1,#init_ori,1 do
        print("init_ori["..(i).."]:", init_ori[i])
    end

    simSetThreadAutomaticSwitch(true)

    -- reset t
    t = 0
end

if (sim_call_type==sim_childscriptcall_initialization) then
    print("--------------------------------")
    print("------Snake initialization------")
    print("--------------------------------") 

    robotHandle=simGetObjectAssociatedWithScript(sim_handle_self)
    
    init_pos = simGetObjectPosition(robotHandle, -1)
    for i=1,#init_pos,1 do
        print("init_pos["..(i).."]:", init_pos[i])
    end

    init_ori = simGetObjectOrientation(robotHandle, -1)
    for i=1,#init_ori,1 do
        print("init_ori["..(i).."]:", init_ori[i])
    end

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
    --print(showCameraView)

    if (showCameraView) then
        --print("Camera view activated")
        floatingView=simFloatingViewAdd(0.2,0.8,0.4,0.4,0)
        simAdjustView(floatingView,cameraHandle,64)
    end

    if (not pluginNotFound) then
        -- Prepare the sensor publisher and the motor speed subscribers:
        turnRadiusSub=simExtRosInterface_subscribe('/turningRadius','std_msgs/Float32','setTurningRadius_cb')
        resetRobotSub=simExtRosInterface_subscribe('/resetRobot','std_msgs/Bool','resetRobot_cb')
    end

    step = 0
    t = 0

    mod = simGetScriptSimulationParameter(sim_handle_self, "mod", true)
    print("mod:\t", mod)

    K = 8
    
    local m = simGetScriptSimulationParameter(sim_handle_self, "m", true)
    print("m:\t", m)

    -- linear reduction parameters (set y = 0 and z = 1 for disabling)
    y = simGetScriptSimulationParameter(sim_handle_self, "y", true)
    print("y:\t", y)

    z = 1 - y

    -- set of control Parameters:
    -- frequency
    w = math.pi*simGetScriptSimulationParameter(sim_handle_self, "w", true)
    print("w:\t", w)

    -- amplitude
    a = math.pi*simGetScriptSimulationParameter(sim_handle_self, "a", true)/180
    print("a:\t", a)

    -- wavelength
    lambda = math.pi*simGetScriptSimulationParameter(sim_handle_self, "lambda", true)/180
    print("lambda:\t", lambda)

    p = -1

    
    local theta = {0,-1,-1,-1,-1,-1,-1,-1,-1}
    local head_dir = 0

    for i=1,K,1 do
        amp = a* ((i-1)*y/K + z)
        theta[i+1] = theta[i] + amp * math.cos(lambda * (i-1))
        head_dir = head_dir + theta[i+1]
    end

    head_dir = head_dir/(K+1)
    print("amp:\t", amp)
    print("head_dir:", head_dir)

    l = 0;
    for i=1,K+1,1 do
        l = l + math.cos(theta[i] - head_dir)
    end

    l = m * l;
    print("l:\t", l)

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
    
    step=step+1
    t=t+simGetSimulationTimeStep()
        
    local theta = 0
    local head_dir = theta

    for i=2,K,1 do
        amp = a * ((i-1)*y/K + z)
        phi = b + amp*math.cos(w*t - lambda * (i-1))
        simSetJointTargetPosition(joints_v[i], -phi*(1-math.exp(p*t)))
        phi = simGetJointPosition(joints_v[i])
        theta = theta + phi
        head_dir = head_dir + theta
    end

    head_dir = head_dir/(K+1)
    
    -- Print parameters every 10 steps
    if(math.fmod(step,mod)==0) then
        print("--------------------------------")
        print("--------Snake step: "..(step).."----------")
        print("--------------------------------")
        print("radius:\t", radius)
        print("b:\t", b)
        print("amp:\t", amp)
        print("phi:\t", phi)
        print("theta:\t", theta)
        print("head_dir:", head_dir)
    end

    -- Head Compensation
    simSetJointTargetPosition(joints_v[1], -head_dir*(1-math.exp(p*t)))
end 
