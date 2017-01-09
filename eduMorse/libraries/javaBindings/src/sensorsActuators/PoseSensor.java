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
public class PoseSensor extends JsonSocketSensor {

    public PoseSensor(String parent, String name, String address, int port) throws IOException {
        super(parent, name, address, port);
        
        codes = new String[7];
        codes[0] = "timestamp";
        codes[1] = "x";
        codes[2] = "y";
        codes[3] = "z";
        codes[4] = "roll";
        codes[5] = "pitch";
        codes[6] = "yaw";
    }

    @Override
    public void sense() throws IOException {
        super.sense();

        double[] res = new double[7];
        for (int i=0 ; i<codes.length ; i++){
            res[i] = (double) jsobj.get(codes[i]);
        }
        sensorList.onSense(res);
    }
}
