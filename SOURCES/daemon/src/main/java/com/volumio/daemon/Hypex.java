package com.volumio.daemon;

import com.pi4j.io.gpio.*;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.core.env.Environment;
import org.springframework.stereotype.Component;

import java.io.IOException;

@Component
public class Hypex {

    Logger logger = LoggerFactory.getLogger(Hypex.class);

    @Autowired
    private Environment env;


    @Value("off")
    private String state;

    String getState() {
        logger.info("State = " + state);
        return state;
    }

    void setState(String state) {

        logger.info("Set state to " + state);

        this.state = state;

        final GpioController gpio = GpioFactory.getInstance();

        switch(state)
        {
            case "on":

                final GpioPinDigitalOutput pin1 = gpio.provisionDigitalOutputPin(RaspiPin.GPIO_03, "AMPON", PinState.LOW);

                break;

            case "off":

                final GpioPinDigitalInput pin2 = gpio.provisionDigitalInputPin(RaspiPin.GPIO_03);

                break;
        }
    }
}
