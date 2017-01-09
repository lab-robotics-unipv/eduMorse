/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package sensorsActuators;

import java.io.IOException;
import org.json.simple.JSONArray;
import org.json.simple.JSONObject;

/**
 *
 * @author daniele
 */
public class IrSensor extends JsonSocketSensor {

    public IrSensor(String parent, String name, String address, int port) throws IOException {
        super(parent, name, address, port);
        
        codes = new String[2];
        codes[0] = "timestamp";
        codes[1] = "range_list";
    }

    @Override
    public void sense() throws IOException {
        super.sense();
        
        double time = (double) jsobj.get(codes[0]);
        JSONArray array2 = (JSONArray) jsobj.get(codes[1]);
        int size = array2.size();
        double[] res = new double[size+1];
        for (int j=0 ; j<size ; j++) {
                        res[j+1] = (double) array2.get(j);
        }
        
        res[0] = time;
        
        sensorList.onSense(res);
    }   
}
