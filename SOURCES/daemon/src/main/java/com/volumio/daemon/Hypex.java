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

    @Autowired
    Volume volume;

    @Autowired
    Screen screen;

    @Value("off")
    private String state;

    GpioPinDigitalOutput gpiopin;

    String getState() {
        logger.info("State = " + state);
        return state;
    }

    public void setState(String state) {

        logger.info("Set state to " + state);

        this.state = state;

        final GpioController gpio = GpioFactory.getInstance();

        if(this.gpiopin == null)
            this.gpiopin = gpio.provisionDigitalOutputPin(RaspiPin.GPIO_09, "AMPON", PinState.HIGH);


        switch(state)
        {
            case "on":
                volume.setVolume(6);
                screen.setOn();
                this.gpiopin.low();
                break;

            case "off":
                screen.setOff();
                this.gpiopin.high();
                break;
        }
    }
}
