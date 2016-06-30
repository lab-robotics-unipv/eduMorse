/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package sensorsActuators;

import java.io.BufferedOutputStream;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.Socket;
import java.util.Map;

/**
 *
 * @author daniele
 */
public abstract class SocketActuator implements Actuator {
    
    protected Socket sock;
    private final BufferedReader input;
    private final BufferedOutputStream output;
    
    protected String req;
    protected String[] codes;

    public SocketActuator(String parent, String name, String address, int port) throws IOException{
        sock = new Socket(address, port);
        input = new BufferedReader(new InputStreamReader(sock.getInputStream()));
        output = new BufferedOutputStream(sock.getOutputStream());
    }
    
    protected String sendRequest(String request) throws IOException {
        request = request.concat("\n");
        
        byte[] bytes = request.getBytes("UTF8");
        output.write(bytes);
        output.flush();
        
        String resp = input.readLine();
                
        int x = isValid(resp, request);
        if (x > 0) {  
            return resp.substring(x);
        } else {
            throw new IOException("Messaggio non inviato correttamente\n");
        }
    }
    
    protected int isValid(String resp, String req) {        
        int space = req.indexOf(" ");
        String success = resp.substring(0, space).concat(" SUCCESS");
        
        if (resp.contains(success)) {
            return success.length();
        }        
        return -1;
    }

    protected boolean messageIsValid(Map map) {
        for (String s : codes) {
            if (! map.containsKey(s))
                return false;
        }
        return true;
    }
    
}
