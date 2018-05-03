function setTurningRadius_cb(msg)
    -- Turning Radius subscriber callback
    radius = msg.data
    
    -- C: Body shape offset, bias value
    -- C = l/(N*r)
    C = 0
    if (radius >= 1 or radius <= -1) then
        C = l/(N*radius) 
    end
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
    end

    -- Prepare Camera handle
    cameraHandle=simGetObjectHandle('DVS_128')
    showCameraView=simGetScriptSimulationParameter(sim_handle_self,'showCameraView')

    if (showCameraView) then
        --print("Camera view activated")
        floatingView=simFloatingViewAdd(0.2,0.8,0.4,0.4,0)
        simAdjustView(floatingView,cameraHandle,64)
    end

    -- Initialize parameters
    step = 0
    t = 0
    mod = simGetScriptSimulationParameter(sim_handle_self, "mod", true)
    r = simGetScriptSimulationParameter(sim_handle_self, "r", true)
    speedChange = simGetScriptSimulationParameter(sim_handle_self, "speedChange", true)
    
    -- Module numbers N?
    N = 8
    
    -- l0 is the length of each module
    local l0 = simGetScriptSimulationParameter(sim_handle_self, "l0", true)
    
    -- linear reduction parameters (set y = 0 and z = 1 for disabling)
    y = simGetScriptSimulationParameter(sim_handle_self, "y", true)
    z = 1 - y

    -- set of control Parameters:

    -- w: temporal frequency: traveling speed of the wave
    w = math.pi*simGetScriptSimulationParameter(sim_handle_self, "w", true)

    -- A: Amplitude
    A = math.pi*simGetScriptSimulationParameter(sim_handle_self, "A", true)/180

    -- Omega: spatial frequency: cycle number of the wave
    Omega = math.pi*simGetScriptSimulationParameter(sim_handle_self, "Omega", true)/180

    -- [Question] What is p? --> for damping
    p = -1

    -- theta k: joint angle --> theta[i]
    local theta = {0,-1,-1,-1,-1,-1,-1,-1,-1}
    
    -- theta snake: global angle of the snake robot --> head_dir
    local head_dir = 0

    -- Snake locomotion
    for i=1,N,1 do
        --[[
        - Linear reduction equation P = ((n/N)*z+y) e [0,1], for all n e [0,N]
        - The amplitude for each joint is defined as a linear function dependent 
            on the module number n
        - The linear coefficient starts at y = 0.3 for the head module and ends 
            at z = 0.7 for the tail module
        - [Question] The sentence above doesn't make a lot of sense to me
            i=1: (1-1)*y/N + z = z =                      8/16
            i=2: (2-1)*y/N + z = 1*y/N + z = 1/16 + 0,5 = 9/16
            i=3: (3-1)*y/N + z = 2*y/N + z = 2/16 + 0,5 = 10/16
            ...
            i=N: ...           = 7*y/N + z = 7/16 + 0,5 = 15/16
        ]]
        P = ((i-1)/N)*y + z

        --[[
        - The joint angle ?k is the result of concatenated local joint angles, 
            which is calculated as: Equation 8 from the Slithering Gait Paper
        - ?k: joint angle --> theta[i]
        - ?: spatial frequency: cycle number of the wave
        - [Question] Why cos instead of sin?
        - [Question] Why amp instead of a (see equation 8)
        ]]
        -- [Comment]
        -- theta[i+1] = theta[i] + P*A*math.(Omega * (i-1))
        theta[i+1] = theta[i] + A*math.sin(Omega * (i-1))
        
        -- ?snake: global angle of the snake robot --> head_dir
        -- ?k: joint angle --> theta[i]
        -- [Question] What is going on here?
        -- Possible answer: head_dir is sum over all joint angles
        head_dir = head_dir + theta[i+1]
    end

    -- ?snake: global angle of the snake robot --> head_dir
    -- [Question] What is going on here?
    -- Possible answer: head_dir is the average value of the joint angles
    head_dir = head_dir/(N+1)

    --[[
    - Body length l = (sum from k=1 to N of lk) = (sum from k=1 to N of l0*cos(?k??snake))
        = l0*(sum from k=1 to N of cos(?k??snake))
    - Each module contributes an effective length that is parallel to the forward 
        direction
    - lk = l0*cos(?k??snake)
    - ?snake: global angle of the snake robot --> head_dir
    - l0 is the length of each module --> m
    - ?k: joint angle --> theta[i]
    ]] 
    l = 0;
    for i=1,N+1,1 do
        l = l + math.cos(theta[i] - head_dir)
    end
    l = l0 * l;

    -- C: Body shape offset, bias value --> b
    -- C = l/(N*r)
    C = 0

    print("--------------------------------")
    print("------Snake initialization------")
    print("--------------------------------")     
    for i=1,#init_pos,1 do
        print("init_pos["..(i).."]:", init_pos[i])
    end
    for i=1,#init_ori,1 do
        print("init_ori["..(i).."]:", init_ori[i])
    end
    print("showCameraView:\t", showCameraView)
    print("w:\t", w)
    print("A:\t", A)
    print("Omega:\t", Omega)
    print("P*A:\t", P*A)
    print("head_dir:", head_dir)
    print("l:\t", l)
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

    -- ?k: joint angle --> theta[i] 
    -- [Question] Why is theta not an array any more?   
    local theta = 0

    -- ?snake: global angle of the snake robot --> head_dir
    -- ?k: joint angle --> theta[i]
    local head_dir = theta

    for i=2,N,1 do
        --[[
        - Linear reduction equation P = ((n/N)*z+y) e [0,1], for all n e [0,N]
        - The amplitude for each joint is defined as a linear function dependent 
            on the module number n
        - The linear coefficient starts at y = 0.3 for the head module and ends 
            at z = 0.7 for the tail module
        ]]
        P = ((i-1)/N)*y + z

        --[[
        - ?(n,t) = C + P*A*sin(?*n+?*t)
        - C: Body shape offset, bias value
        - P: Linear dependency, linear reduction equation P (see above) \__ P*A 
        - A: Amplitude                                                  /
        - ?: spatial frequency: cycle number of the wave
        - ?: temporal frequency: traveling speed of the wave --> w
        - [Question] Why cos instead of sin?
        - [Question] Why i-1 ?
        - [Question] Why - instead of +? --> so that the snake moves forward
        ]]
        -- [Comment]
        -- phi = C + P*A*math.cos(w*t - Omega*(i-1))
        phi = C + P*A*math.sin(Omega*(i-1) - w*t)
        
        -- [Question] Why -phi*(1-math.exp(p*t)) ?
        -- [Comment]
        simSetJointTargetPosition(joints_v[i], -phi*(1-math.exp(p*t)))
        -- simSetJointTargetPosition(joints_v[i], phi)
        
        phi = simGetJointPosition(joints_v[i])

        --[[
        The joint angle ?k is the result of concatenated local joint angles, 
            which is calculated as: Equation 8 from the Slithering Gait Paper
        ]]
        theta = theta + phi

        --[[
        - The compensation angle for the joint module is ?, the joint angle for the 
            kth module is ?k. Therefore, in the global coordinates, the ith module 
            angle can be calculated as: Equation 11 from the Slithering Gait Paper
        - ?snake: global angle of the snake robot --> head_dir
        - ?k: joint angle --> theta[i]
        ]]
        head_dir = head_dir + theta
    end

    -- Then we can derive the compensation angle ? as: Equation 14 from the Slithering Gait Paper
    -- ?snake: global angle of the snake robot --> head_dir
    head_dir = head_dir/(N+1)
    
    -- Head Compensation
    -- [Question] Why *(1-math.exp(p*t))? --> damping
    -- [Comment]
    simSetJointTargetPosition(joints_v[1], -head_dir*(1-math.exp(p*t)))
    -- simSetJointTargetPosition(joints_v[1], -head_dir)

    -- Print parameters every mod steps
    if(math.fmod(step,mod)==0) then
        print("--------------------------------")
        print("--------Snake step: "..(step).."----------")
        print("--------------------------------")
        print("dist:\t", dist)
        print("w:\t", w)
        print("t:\t", t)
        print("radius:\t", radius)
        print("C:\t", C)
        print("P*A:\t", P*A)
        print("phi:\t", phi)
        print("theta:\t", theta)
        print("head_dir:", head_dir)
    end
end