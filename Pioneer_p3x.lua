function turn()
    if(turnRight == true) then
        simSetJointTargetVelocity(motorRight,v0+speedIncrease)
        simSetJointTargetVelocity(motorLeft,0)
    else
        simSetJointTargetVelocity(motorLeft,v0+speedIncrease)
        simSetJointTargetVelocity(motorRight,0)
    end
end

function endTurn()
    simSetJointTargetVelocity(motorRight,v0)
    simSetJointTargetVelocity(motorLeft,v0)
end

function publishParameters()
    data = {}
    parameters = '{"Pioneer parameters":' .. '{' .. '"v0": ' .. v0 .. ', "turnLength": ' .. turnLength .. ', "turnFrequency": ' .. turnFrequency .. '}}'
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

    simSetObjectPosition(robotHandle,-1,init_pos)
    simSetObjectOrientation(robotHandle,-1,init_ori)

    simSetThreadAutomaticSwitch(true)
    
    -- reset t, turnRight and step
    t = 0
    turnRight = true
    step = 0

    if (comments == true) then
        print("--------------------------------")
        print("-------Reset Pioneer_p3dx-------")
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
    motorLeft=simGetObjectHandle("Pioneer_p3dx_leftMotor")
    motorRight=simGetObjectHandle("Pioneer_p3dx_rightMotor")

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
        resetRobotSub=simExtRosInterface_subscribe('/resetRobot','std_msgs/Bool','resetRobot_cb')
        paramsPub=simExtRosInterface_advertise('/parameters', 'std_msgs/String')
    end

    -- Initialize parameters
    comments = simGetScriptSimulationParameter(sim_handle_self, "comments")
    randomNumber = 0
    turning = false
    turnRight = true
    turnLength = simGetScriptSimulationParameter(sim_handle_self, "turnLength")
    stepsLeft = turnLength
    turnFrequency = simGetScriptSimulationParameter(sim_handle_self, "turnFrequency")
    speedIncrease = 0
    step = 0
    t = 0
    mod = simGetScriptSimulationParameter(sim_handle_self, "mod")
    v0 = simGetScriptSimulationParameter(sim_handle_self, "v0")
    
    -- Start movement
    simSetJointTargetVelocity(motorRight,v0)
    simSetJointTargetVelocity(motorLeft,v0)

    if (comments == true) then
        print("--------------------------------")
        print("-----Pioneer initialization-----")
        print("--------------------------------")
        for i=1,#init_pos,1 do
            print("init_pos["..(i).."]:", init_pos[i])
        end
        for i=1,#init_ori,1 do
            print("init_ori["..(i).."]:", init_ori[i])
        end
        print("mod:\t", mod)
        print("v0:\t", v0)
    end    
end 

if (sim_call_type==sim_childscriptcall_actuation) then 

    if(step == 1) then
        publishParameters()
    end

    step=step+1
    t=t+simGetSimulationTimeStep()

    pos = simGetObjectPosition(robotHandle, -1)
    ori = simGetObjectOrientation(robotHandle, -1)
    
    -- Turning functionality: every turnFrequency steps the right or  
    -- left motor speed is increasedby speedIncrease for turnLength steps
   
    -- Turn every turnFrequency steps
    if(math.fmod(step,turnFrequency)==0) then
        turning = true
        math.randomseed(os.time())
        randomNumber = math.random()
        -- speedIncrease = math.fmod(randomNumber * 100, v0/2)
        speedIncrease = v0/4
    end
    
    -- As long as turning is true
    if(turning == true) then
        -- If stepsLeft equals turnLength, call turn function
        if(stepsLeft == turnLength) then 
            turn()
        end
        -- Decrease stepsLeft
        stepsLeft = stepsLeft - 1
    end
    
    -- If stepsLeft equals 0
    if(stepsLeft == 0) then
        -- turning is set to false
        turning = false
        -- turnRight is set to the opposite, so the next turn goes in opposite direction
        turnRight = not turnRight
        -- stepsLeft is resetted to turnLength
        stepsLeft = turnLength
        -- endTurn function is called
        endTurn()
    end
        
    if((comments == true) and (math.fmod(step,mod)==0)) then
        print("--------------------------------")
        print("--------Pioneer step: "..(step).."--------")
        print("--------------------------------")
        print("t:\t", t)
        for i=1,#pos,1 do
            print("pos["..(i).."]:\t", pos[i])
        end
        for i=1,#ori,1 do
            print("ori["..(i).."]:\t", ori[i])
        end
    end
end
