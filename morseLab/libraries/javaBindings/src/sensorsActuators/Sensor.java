/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package sensorsActuators;

import java.io.IOException;

/**
 *
 * @author daniele
 */
public abstract class Sensor {

    protected SensorListener sensorList;
    
    /**
     *
     * @throws java.io.IOException
     */
    public abstract void sense() throws IOException;
    
    void setSensorListener(SensorListener sl) {
        sensorList = sl;
    }
}
