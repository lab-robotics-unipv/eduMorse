package sensorsActuators;

import java.io.IOException;
import java.util.Map;

/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
/**
 *
 * @author daniele
 */
public interface Actuator {

    void act(Map map) throws IOException;
}
