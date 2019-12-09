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

        if(input != this.input) {
            dsp.setInput(input);
            volumio.setInput(input);
            this.input = input;
        }
        else
            logger.info("input unchanged, ignoring");
    }
}
