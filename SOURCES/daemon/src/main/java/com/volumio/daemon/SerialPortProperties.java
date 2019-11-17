package com.volumio.daemon;

import lombok.Data;
import lombok.NonNull;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.stereotype.Component;

@Component
@ConfigurationProperties(prefix = "spring-serial-port-connector")
public @Data
class SerialPortProperties {

    /**
     * Port used in the application
     */
    private String portName;

    /**
     * This is the baudRate to use for read and write data in the serial port
     */
    private int baudRate;

    public String getPortName() {
        return this.portName;
    }

    public int getBaudRate() {
        return this.baudRate;
    }
}