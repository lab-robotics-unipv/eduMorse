/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package sensorsActuators;

import java.io.IOException;
import org.json.simple.JSONObject;
import org.json.simple.JSONValue;

/**
 *
 * @author daniele
 */
public abstract class JsonSocketSensor extends SocketSensor {
    
    protected final String req;
    protected String[] codes;
    protected JSONObject jsobj;

    public JsonSocketSensor(String parent, String name, String address, int port) throws IOException {
        super(address, port);
        req = "id1 " + parent + "." + name + " get_local_data";
    }

    @Override
    public void sense() throws IOException {
        String risp = sendRequest(req);
        
        Object obj = JSONValue.parse(risp);
        jsobj = JSONObject.class.cast(obj);
                
        if (! messageIsValid(jsobj))
            throw new IOException("Messaggio non codificato correttamente\n");
    }
    
    private boolean messageIsValid(JSONObject JS) {
        for (String s : codes) {
            if (! JS.containsKey(s))
                return false;
        }   
        return true;
    }
}
