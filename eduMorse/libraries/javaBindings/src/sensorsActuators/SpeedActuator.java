
/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package sensorsActuators;

import java.io.IOException;
import java.util.Locale;
import java.util.Map;

/**
 *
 * @author daniele
 */
public class SpeedActuator extends SocketActuator {

    public SpeedActuator(String parent, String name, String address, int port) throws IOException {
        super(parent, name, address, port);
        req = "id1 " + parent + "." + name + " set_speed [%,f,%,f]";
        
        codes = new String[2];
        codes[0] = "linVel";
        codes[1] = "angVel";
    }
    
    @Override
    public void act(Map map) throws IOException {
        if (! messageIsValid(map)) 
            throw new ClassFormatError("Formato messaggio errato");        
        sendRequest(String.format(Locale.US, req, map.get(codes[0]), map.get(codes[1])));
    }  
}
