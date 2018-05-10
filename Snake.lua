function setTurningRadius_cb(msg)
    -- Turning Radius subscriber callback
    radius = msg.data
    
    C = 0
    if (radius >= 1 or radius <= -1) then
        C = l/(N*radius) 
    end
end

function publishParameters()
    data = {}
    parameters = '{"Snake parameters":{' .. '"speedChange": ' .. speedChange .. '}}'
    data['data'] = parameters
    simExtRosInterface_publish(paramsPub,data)
end

function resetRobot_cb(msg)
    -- Reset robot subscriber callback
    -- get all objects in the model
    allModelObjects=simGetObjectsInTree(robotHandle) 

    simSetThreadAutomaticSwitch(false)
  
    -- reset all objects in the model
    for i=1,#allModelObjects,1 do
        simResetDynamicObject(allModelObjects[i])
    end

    for i=1,N,1 do
        simSetJointPosition(joints_v[i], 0)
        simSetJointTargetPosition(joints_v[i], 0)
    end

    simSetObjectPosition(robotHandle,-1,init_pos)
    simSetObjectOrientation(robotHandle,-1,init_ori)

    simSetThreadAutomaticSwitch(true)

    -- reset t
    t = 0

    if (comments == true) then
        print("--------------------------------")
        print("----------Reset Snake-----------")
        print("--------------------------------")
        for i=1,#init_pos,1 do
            print("init_pos["..(i).."]:", init_pos[i])
        end
        for i=1,#init_ori,1 do
            print("init_ori["..(i).."]:", init_ori[i])
        end
    end
end

if (sim_call_type==sim_childscriptcall_initialization) then

    -- Get object handles
    robotHandle=simGetObjectAssociatedWithScript(sim_handle_self)
    proxSensor=simGetObjectHandle("Snake_proxSensor")

    joints_v={-1,-1,-1,-1,-1,-1,-1,-1}

    for i=1,8,1 do
        joints_v[i]=simGetObjectHandle('Snake_vJoint_'..(i))
    end
    
    -- Get init position and orientation
    init_pos = simGetObjectPosition(robotHandle, -1)
    init_ori = simGetObjectOrientation(robotHandle, -1)

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

    if (not pluginNotFound) then
        -- Prepare the sensor publisher and the motor speed subscribers:
        turnRadiusSub=simExtRosInterface_subscribe('/turningRadius','std_msgs/Float32','setTurningRadius_cb')
        resetRobotSub=simExtRosInterface_subscribe('/resetRobot','std_msgs/Bool','resetRobot_cb')
        paramsPub=simExtRosInterface_advertise('/parameters', 'std_msgs/String')
    end

    -- Prepare Camera handle
    cameraHandle=simGetObjectHandle('DVS_128')
    showCameraView=simGetScriptSimulationParameter(sim_handle_self,'showCameraView')

    if (showCameraView) then
        floatingView=simFloatingViewAdd(0.2,0.8,0.4,0.4,0)
        simAdjustView(floatingView,cameraHandle,64)
    end

    -- Initialize parameters
    comments = simGetScriptSimulationParameter(sim_handle_self, "comments")
    step = 0
    t = 0
    mod = simGetScriptSimulationParameter(sim_handle_self, "mod")
    speedChange = simGetScriptSimulationParameter(sim_handle_self, "speedChange")
    
    N = 8
    
    local l0 = simGetScriptSimulationParameter(sim_handle_self, "l0")
    
    -- linear reduction parameters (set y = 0 and z = 1 for disabling)
    y = simGetScriptSimulationParameter(sim_handle_self, "y")
    z = 1 - y

    -- set of control Parameters:

    -- w: temporal frequency: traveling speed of the wave
    w = math.pi*simGetScriptSimulationParameter(sim_handle_self, "w")
    -- A: Amplitude
    A = math.pi*simGetScriptSimulationParameter(sim_handle_self, "A")/180
    -- Omega: spatial frequency: cycle number of the wave
    Omega = math.pi*simGetScriptSimulationParameter(sim_handle_self, "Omega")/180
    -- for damping
    p = -1

    -- theta k: joint angle --> theta[i]
    local theta = {0,-1,-1,-1,-1,-1,-1,-1,-1}
    -- theta snake: global angle of the snake robot --> head_dir
    local head_dir = 0

    -- Snake locomotion
    for i=1,N,1 do
        -- Linear reduction equation P = ((n/N)*z+y) e [0,1], for all n e [0,N]
        P = ((i-1)/N)*y + z

        -- theta[i+1] = theta[i] + P*A*math.(Omega * (i-1))
        theta[i+1] = theta[i] + A*math.sin(Omega * (i-1))
        
        head_dir = head_dir + theta[i+1]
    end

    -- [Question] What is going on here?
    -- Possible answer: head_dir is the average value of the joint angles
    head_dir = head_dir/(N+1)

    l = 0;
    for i=1,N+1,1 do
        l = l + math.cos(theta[i] - head_dir)
    end
    l = l0 * l;

    C = 0

    if (comments == true) then
        print("--------------------------------")
        print("------Snake initialization------")
        print("--------------------------------")     
        for i=1,#init_pos,1 do
            print("init_pos["..(i).."]:", init_pos[i])
        end
        for i=1,#init_ori,1 do
            print("init_ori["..(i).."]:", init_ori[i])
        end
        print("w:\t", w)
        print("A:\t", A)
        print("Omega:\t", Omega)
        print("P*A:\t", P*A)
        print("head_dir:", head_dir)
        print("l:\t", l)
    end
end 

if (sim_call_type==sim_childscriptcall_cleanup) then 
    if not pluginNotFound then
        -- Following not really needed in a simulation script 
        -- (i.e. automatically shut down at simulation end):
        simExtRosInterface_shutdownSubscriber(turnRadiusSub)
        simExtRosInterface_shutdownSubscriber(resetRobotSub)
    end

    if auxConsole then
        simAuxiliaryConsoleClose(auxConsole)
    end
end

if (sim_call_type==sim_childscriptcall_actuation) then
    if(step == 1) then 
        publishParameters()
    end
    step=step+1
    t=t+simGetSimulationTimeStep()
    
    -- Read res (-1, 0 or 1) and dist from proxSensor
    res, dist = simReadProximitySensor(proxSensor)
    
    -- Proximity functionality
    -- If proxSensor senses an object
    if (res == 1) then
        -- If distance below 1.5, slow down
        if(dist < 1.5) then
            w = w - speedChange
        -- If distance above 3, speed up
        elseif(dist > 3) then
            w = w + speedChange
        end
    end

    -- Snake locomotion

    -- [Question] Why is theta not an array any more?   
    local theta = 0

    local head_dir = theta

    for i=2,N,1 do

        P = ((i-1)/N)*y + z

        -- phi = C + P*A*math.cos(w*t - Omega*(i-1))
        phi = C + P*A*math.sin(Omega*(i-1) - w*t)
        
        -- [Question] Why -phi*(1-math.exp(p*t)) ?
        -- [Comment]
        simSetJointTargetPosition(joints_v[i], -phi*(1-math.exp(p*t)))
        
        phi = simGetJointPosition(joints_v[i])

        theta = theta + phi

        head_dir = head_dir + theta
    end

    head_dir = head_dir/(N+1)
    
    simSetJointTargetPosition(joints_v[1], -head_dir*(1-math.exp(p*t)))

    -- Print parameters every mod steps
    if(comments==true and math.fmod(step,mod)==0) then
        print("--------------------------------")
        print("--------Snake step: "..(step).."----------")
        print("--------------------------------")
        print("dist:\t", dist)
        print("radius:\t", radius)
        print("w:\t", w)
    end
end
