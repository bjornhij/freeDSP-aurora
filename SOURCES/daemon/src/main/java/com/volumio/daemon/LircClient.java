package com.volumio.daemon;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.stereotype.Service;

import java.io.BufferedReader;
import java.io.DataOutputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.Socket;
import java.util.concurrent.PriorityBlockingQueue;

@Service("socketClient")

public class LircClient {
    @Value("${lirc.tcpPort}")
    int tcpPort;

    @Value("${lirc.ipConnection}")
    String ipConnection;

    private Socket clientSocket;

    private DataOutputStream outToTCP;
    private BufferedReader inFromTCP;

    private PriorityBlockingQueue<String> incomingMessages = new PriorityBlockingQueue<>();
    private PriorityBlockingQueue<String> outcomingMessages = new PriorityBlockingQueue<>();

    private final Logger log = LoggerFactory.getLogger(this.getClass());

    private Thread sendDataToTCP = new Thread(){
        public void run(){
            String sentence = "";
            log.info("Starting Backend -> TCP communication thread");
            while(true){
                try {
                    sentence = incomingMessages.take();
                    outToTCP.writeBytes(sentence + '\n');
                } catch (InterruptedException e) {
                    e.printStackTrace();
                } catch (IOException e) {
                    e.printStackTrace();
                }

            }
        }
    };

    private Thread getDataFromTCP = new Thread(){
        public void run(){
            log.info("Starting TCP -> Backend communication thread");
            while(true){
                String response = "";
                try {
                    response = inFromTCP.readLine();
                    if (response == null)
                        break;

                    log.info("Lirc sent " + response);

                    outcomingMessages.put(response);
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        }
    };

    public void openConnection(){
        try {
            this.clientSocket = new Socket(ipConnection, tcpPort);
            outToTCP = new DataOutputStream(clientSocket.getOutputStream());
            inFromTCP = new BufferedReader(new InputStreamReader(clientSocket.getInputStream()));
            getDataFromTCP.start();
            sendDataToTCP.start();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    //Send messages to Socket.
    public void sendMessage(String message) throws InterruptedException {
        incomingMessages.put(message);
    }
    //Take Message from Socket
    public String takeMessage() throws InterruptedException {
        return outcomingMessages.take();
    }
}
