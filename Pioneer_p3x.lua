function resetRobot_cb(msg)
    -- Reset robot subscriber callback
    allModelObjects=simGetObjectsInTree(robotHandle) -- get all objects in the model
    simSetThreadAutomaticSwitch(false)
    for i=1,#allModelObjects,1 do
        simResetDynamicObject(allModelObjects[i]) -- reset all objects in the model
    end
    simSetObjectPosition(robotHandle,-1,init_pos)
    simSetObjectOrientation(robotHandle,-1,init_ori)
    simSetThreadAutomaticSwitch(true)
end

if (sim_call_type==sim_childscriptcall_initialization) then 
    
    robotHandle=simGetObjectAssociatedWithScript(sim_handle_self)
    
    init_pos = simGetObjectPosition(robotHandle, -1)
    init_ori = simGetObjectOrientation(robotHandle, -1)

    motorLeft=simGetObjectHandle("Pioneer_p3dx_leftMotor")
    motorRight=simGetObjectHandle("Pioneer_p3dx_rightMotor")
   
    step = 0
    t = 0
    vOffset = 0
    amp = simGetScriptSimulationParameter(sim_handle_self, "amp", true) 
    w = math.pi*simGetScriptSimulationParameter(sim_handle_self, "w", true)  
    v0 = simGetScriptSimulationParameter(sim_handle_self, "v0", true) 

    if (not pluginNotFound) then
        resetRobotSub=simExtRosInterface_subscribe('/resetRobot','std_msgs/Bool','resetRobot_cb')
    end
end 

if (sim_call_type==sim_childscriptcall_cleanup) then 
 
end 

if (sim_call_type==sim_childscriptcall_actuation) then 
    
    step=step+1
    t=t+simGetSimulationTimeStep()

    vOffset = amp*math.cos(w*t)

    vLeft=v0+vOffset
    vRight=v0-vOffset
       
    simSetJointTargetVelocity(motorLeft,vLeft)
    simSetJointTargetVelocity(motorRight,vRight)

    if(math.fmod(step,5)==0) then
        print("---------",step,"--------")
        print("t\t", t)
        print("vOffset:", vOffset)
        print("vLeft:\t", vLeft)
        print("vRight:\t", vRight)
        print("--------------------------------")
    end
end 