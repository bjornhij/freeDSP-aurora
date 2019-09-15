package com.volumio.daemon;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

@Component
public class Volume {
    Logger logger = LoggerFactory.getLogger(Volume.class);

    private int volume = 0;

    @Autowired
    Dsp dsp;

    @Autowired
    Volumio volumio;

    public int getVolume() {
        return dsp.getVolume();
    }

    public void setVolume(int volume) {
        logger.info("Current volume is " + this.volume);
        logger.info("Setting to " + volume + " linear");

        if(volume != this.volume) {
            dsp.setVolume(volume);
            volumio.setVolume(volume);
            this.volume = volume;
        }
        else
            logger.info("Volume unchanged, ignoring");
    }
}
