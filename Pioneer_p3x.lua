function resetRobot_cb(msg)
    -- Reset robot subscriber callback
    print("--------------------------------")
    print("-------Reset Pioneer_p3dx-------")
    print("--------------------------------")
    
    -- get all objects in the model
    allModelObjects=simGetObjectsInTree(robotHandle) 
    simSetThreadAutomaticSwitch(false)
    
    -- reset all objects in the model
    for i=1,#allModelObjects,1 do
        simResetDynamicObject(allModelObjects[i]) 
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
    print("-----Pioneer initialization-----")
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

    motorLeft=simGetObjectHandle("Pioneer_p3dx_leftMotor")
    motorRight=simGetObjectHandle("Pioneer_p3dx_rightMotor")
   
    step = 0
    t = 0
    
    mod = simGetScriptSimulationParameter(sim_handle_self, "mod", true)
    print("mod:\t", mod)

    vOffset = 0
    
    A = simGetScriptSimulationParameter(sim_handle_self, "A", true)
    print("A:\t", A)

    w = simGetScriptSimulationParameter(sim_handle_self, "w", true)
    print("w:\t", w)

    v0 = simGetScriptSimulationParameter(sim_handle_self, "v0", true)
    print("v0:\t", v0)

    if (not pluginNotFound) then
        resetRobotSub=simExtRosInterface_subscribe('/resetRobot','std_msgs/Bool','resetRobot_cb')
    end
end 

if (sim_call_type==sim_childscriptcall_cleanup) then 
 
end 

if (sim_call_type==sim_childscriptcall_actuation) then 
    
    step=step+1
    t=t+simGetSimulationTimeStep()

    vOffset = A*math.sin(w*t)

    vLeft=v0+vOffset
    vRight=v0-vOffset
       
    simSetJointTargetVelocity(motorLeft,vLeft)
    simSetJointTargetVelocity(motorRight,vRight)

    pos = simGetObjectPosition(robotHandle, -1)
    ori = simGetObjectOrientation(robotHandle, -1)
        
    if(math.fmod(step,mod)==0) then
        print("--------------------------------")
        print("--------Pioneer step: "..(step).."--------")
        print("--------------------------------")
        print("t:\t", t)
        print("w*t:\t", w*t)
        print("vOffset:", vOffset)
        print("vLeft:\t", vLeft)
        print("vRight:\t", vRight)
        for i=1,#pos,1 do
            print("pos["..(i).."]:\t", pos[i])
        end
        for i=1,#ori,1 do
            print("ori["..(i).."]:\t", ori[i])
        end
    end
end 