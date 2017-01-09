/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package sensorsActuators;

import java.io.IOException;
import static java.lang.reflect.Array.set;
import java.sql.DriverManager;
import java.util.HashMap;
import java.util.Map;
import java.util.Set;
import org.json.simple.JSONObject;
import org.json.simple.JSONValue;

/**
 *
 * @author daniele
 */
public class DistanceSensor extends JsonSocketSensor {

    public DistanceSensor(String parent, String name, String address, int port) throws IOException {
        super(parent, name, address, port);

        codes = new String[2];
        codes[0] = "timestamp";
        codes[1] = "near_objects";
        // codes[2] = "near_robots";
    }

    @Override
    public void sense() throws IOException {
        super.sense();

        sensorList.onSense((double) jsobj.get(codes[0]));

        Map<String, Double> objs = new HashMap<>();
        // Map<String, Double> robs = new HashMap<>();

        JSONObject JsObjs = (JSONObject) jsobj.get(codes[1]);
        // JSONObject JsRobs = (JSONObject) jsobj.get(codes[2]);

        Set objNames = JsObjs.keySet();
        for (Object s : objNames) {
            objs.put((String) s, (double) JsObjs.get((String) s));
        }

//        Set robNames = JsRobs.keySet();
//        for (Object s : robNames) {
//            robs.put((String) s, (double) JsRobs.get((String) s));
//        }

        sensorList.onSense("objects", (HashMap<String, Double>) objs);
        // sensorList.onSense("robots", (HashMap<String, Double>) robs);
    }
}
