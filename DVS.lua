if (sim_call_type==sim_childscriptcall_initialization) then
    -- Get some handles:
    VisionSensor=simGetObjectHandle('DVS_128')

    -- Enable an image publisher and subscriber:
    pub=simExtRosInterface_advertise('/redImage', 'sensor_msgs/Image')
    simExtRosInterface_publisherTreatUInt8ArrayAsString(pub) -- treat uint8 arrays as strings (much faster, tables/arrays are kind of slow in Lua)
end

if (sim_call_type==sim_childscriptcall_sensing) then
    -- Publish the image of the active vision sensor:
    local data,w,h=simGetVisionSensorCharImage(VisionSensor)
    d={}
    d['header']={seq=0,stamp=simExtRosInterface_getTime(), frame_id="a"}
    d['height']=h
    d['width']=w
    d['encoding']='rgb8'
    d['is_bigendian']=1
    d['step']=w*3
    d['data']=data
    simExtRosInterface_publish(pub,d)
end

if (sim_call_type==sim_childscriptcall_cleanup) then
    -- Shut down publisher and subscriber. Not really needed from a simulation script (automatic shutdown)
    simExtRosInterface_shutdownPublisher(pub)
end