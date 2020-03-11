package com.volumio.daemon;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import java.io.IOException;

@Component
public class Screen {

    Logger logger = LoggerFactory.getLogger(Volume.class);

    private int max_brightnes = 80;

    public void setOn() {

        logger.info("Screen on");

        for(int i = 0; i <= this.max_brightnes; i++) {

            try {
                String[] cmd = {
                        "/bin/bash",
                        "-c",
                        "/bin/echo " + i + " > /sys/class/backlight/rpi_backlight/brightness"
                };

                Process process = Runtime.getRuntime()
                        .exec(cmd);

            }
            catch (IOException e)
            {

            }
        }
    }

    public void setOff() {

        logger.info("Screen off");

        for(int i = this.max_brightnes; i >= 0; i--) {

            try {
                String[] cmd = {
                        "/bin/bash",
                        "-c",
                        "/bin/echo " + i + " > /sys/class/backlight/rpi_backlight/brightness"
                };

                Process process = Runtime.getRuntime()
                        .exec(cmd);
            }
            catch (IOException e)
            {

            }
        }
    }


}
