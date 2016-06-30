/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package sensorsActuators;

import java.util.HashMap;

/**
 *
 * @author daniele
 */
public interface SensorListener {
    void onSense(int meas);
    void onSense(double meas);
    void onSense(double[] meas);
    void onSense(String s, HashMap<String, Double> map);
}
