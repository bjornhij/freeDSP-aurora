package com.volumio.daemon;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

@Component
public class Input {
    Logger logger = LoggerFactory.getLogger(Volume.class);

    private String input = "";

    @Autowired
    Dsp dsp;

    @Autowired
    Volumio volumio;

    public String getInput() {
        return dsp.getInput();
    }

    public void setInput(String input) {

        logger.info("Current input is " + this.input);
        logger.info("Setting to " + input);

        if(!input.equals(this.input)) {
            this.input = input;
            dsp.setInput(input);

            if(!input.equals("usb")) {
                logger.info("Setting volumio to " + input);
                volumio.setInput(input);
            }
        }
        else
            logger.info("input unchanged, ignoring");
    }
}
