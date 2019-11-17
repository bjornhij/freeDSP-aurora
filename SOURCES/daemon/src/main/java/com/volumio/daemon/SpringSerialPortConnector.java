package com.volumio.daemon;

import gnu.io.SerialPortEventListener;

import java.io.IOException;

public interface SpringSerialPortConnector extends SerialPortEventListener {

    void sendMessage(String message) throws IOException;
}