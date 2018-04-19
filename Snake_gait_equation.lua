function setTurningRadius_cb(msg)
    -- Turning Radius subscriber callback
    radius = msg.data
    
    -- C: Body shape offset, bias value --> b
    -- C = l/(N*r)
    b = 0
    if (radius >= 1 or radius <= -1) then
        b = l / (N*radius) 
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

    for i=1,N,1 do
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

    if (not pluginNotFound) then
        -- Prepare the sensor publisher and the motor speed subscribers:
        turnRadiusSub=simExtRosInterface_subscribe('/turningRadius','std_msgs/Float32','setTurningRadius_cb')
        resetRobotSub=simExtRosInterface_subscribe('/resetRobot','std_msgs/Bool','resetRobot_cb')
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

    step = 0
    t = 0

    mod = simGetScriptSimulationParameter(sim_handle_self, "mod", true)
    
    -- Module numbers N?
    N = 8
    
    -- l0 is the length of each module --> m
    local m = simGetScriptSimulationParameter(sim_handle_self, "m", true)
    
    -- linear reduction parameters (set y = 0 and z = 1 for disabling)
    y = simGetScriptSimulationParameter(sim_handle_self, "y", true)
    z = 1 - y

    -- set of control Parameters:

    -- ω: temporal frequency: traveling speed of the wave --> w
    w = math.pi*simGetScriptSimulationParameter(sim_handle_self, "w", true)
    print("w:\t", w)

    -- A: Amplitude
    a = math.pi*simGetScriptSimulationParameter(sim_handle_self, "a", true)/180
    print("a:\t", a)

    -- Ω: spatial frequency: cycle number of the wave --> lambda
    lambda = math.pi*simGetScriptSimulationParameter(sim_handle_self, "lambda", true)/180
    print("lambda:\t", lambda)

    -- [Question] What is p?
    p = -1

    -- θk: joint angle --> theta[i]
    local theta = {0,-1,-1,-1,-1,-1,-1,-1,-1}
    
    -- θsnake: global angle of the snake robot --> head_dir
    local head_dir = 0

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
        amp = a * ((i-1)*y/N + z)

        --[[
        - The joint angle θk is the result of concatenated local joint angles, 
            which is calculated as: Equation 8 from the Slithering Gait Paper
        - θk: joint angle --> theta[i]
        - Ω: spatial frequency: cycle number of the wave --> lambda
        - [Question] Why cos instead of sin?
        ]]
        theta[i+1] = theta[i] + amp * math.cos(lambda * (i-1))
        
        -- θsnake: global angle of the snake robot --> head_dir
        -- θk: joint angle --> theta[i]
        -- [Question] What is going on here?
        -- Possible answer: head_dir is sum over all joint angles
        head_dir = head_dir + theta[i+1]
    end

    -- θsnake: global angle of the snake robot --> head_dir
    -- [Question] What is going on here?
    -- Possible answer: head_dir is the average value of the joint angles
    head_dir = head_dir/(N+1)

    print("amp:\t", amp)
    print("head_dir:", head_dir)

    --[[
    - Body length l = (sum from k=1 to N of lk) = (sum from k=1 to N of l0*cos(θk−θsnake))
        = l0*(sum from k=1 to N of cos(θk−θsnake))
    - Each module contributes an effective length that is parallel to the forward 
        direction
    - lk = l0*cos(θk−θsnake)
    - θsnake: global angle of the snake robot --> head_dir
    - l0 is the length of each module --> m
    - θk: joint angle --> theta[i]
    ]] 
    l = 0;
    for i=1,N+1,1 do
        l = l + math.cos(theta[i] - head_dir)
    end
    l = m * l;
    print("l:\t", l)

    -- C: Body shape offset, bias value --> b
    -- C = l/(N*r)
    b = 0
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
    
    -- θk: joint angle --> theta[i] 
    -- [Question] Why is theta not an array any more?   
    local theta = 0

    -- θsnake: global angle of the snake robot --> head_dir
    -- θk: joint angle --> theta[i]
    local head_dir = theta

    for i=2,N,1 do
        
        --[[
        - Linear reduction equation P = ((n/N)*z+y) e [0,1], for all n e [0,N]
        - The amplitude for each joint is defined as a linear function dependent 
            on the module number n
        - The linear coefficient starts at y = 0.3 for the head module and ends 
            at z = 0.7 for the tail moduleThe linear coefficient starts at 
            y = 0.3 for the head module and ends at z = 0.7 for the tail module
        ]]
        amp = a * ((i-1)*y/N + z)

        --[[
        - φ(n,t) = C + P*A*sin(Ω*n+ω*t)
        - C: Body shape offset, bias value --> b
        - P: Linear dependency, linear reduction equation P (see above) \__ P*A
        - A: Amplitude                                                  /
        - Ω: spatial frequency: cycle number of the wave --> lambda
        - ω: temporal frequency: traveling speed of the wave --> w
        - [Question] Why cos instead of sin?
        ]]
        phi = b + amp*math.cos(w*t - lambda*(i-1))
        
        -- [Question] Why -phi*(1-math.exp(p*t)) ?
        simSetJointTargetPosition(joints_v[i], -phi*(1-math.exp(p*t)))
        
        phi = simGetJointPosition(joints_v[i])

        --[[
        The joint angle θk is the result of concatenated local joint angles, 
            which is calculated as: Equation 8 from the Slithering Gait Paper
        ]]
        theta = theta + phi

        --[[
        - The compensation angle for the joint module is β, the joint angle for the 
            kth module is θk. Therefore, in the global coordinates, the ith module 
            angle can be calculated as: Equation 11 from the Slithering Gait Paper
        - θsnake: global angle of the snake robot --> head_dir
        - θk: joint angle --> theta[i]
        ]]
        head_dir = head_dir + theta
    end

    -- Then we can derive the compensation angle β as: Equation 14 from the Slithering Gait Paper
    -- θsnake: global angle of the snake robot --> head_dir
    head_dir = head_dir/(N+1)
    
    -- Head Compensation
    -- [Question] Why *(1-math.exp(p*t))?
    simSetJointTargetPosition(joints_v[1], -head_dir*(1-math.exp(p*t)))

    -- Print parameters every 10 steps
    if(math.fmod(step,mod)==0) then
        print("--------------------------------")
        print("--------Snake step: "..(step).."----------")
        print("--------------------------------")
        print("t:\t", t)
        print("radius:\t", radius)
        print("b:\t", b)
        print("amp:\t", amp)
        print("phi:\t", phi)
        print("theta:\t", theta)
        print("head_dir:", head_dir)
    end
end 