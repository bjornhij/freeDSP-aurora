package com.volumio.daemon;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.core.env.Environment;
import org.springframework.stereotype.Component;

import java.io.IOException;

@Component
public class Dsp extends AbstractSpringSerialPortConnector {

    Logger logger = LoggerFactory.getLogger(Dsp.class);

    @Autowired
    private Environment env;

    private int volume = 0;

    @Value("${volumiodaemon.initial_input}")
    private String input;

    int getVolume() {
        logger.info("Volume = " + volume);
        return volume;
    }

    void setVolume(int volume) {

        logger.info("Set volume to " + volume);

        // http://www.playdotsound.com/portfolio-item/decibel-db-to-float-value-calculator-making-sense-of-linear-values-in-audio-tools/
        // linear-to-db(x) = log(x) * 20

        this.volume = volume;

        double dsp_volume = Math.log(volume / 100.0) * 20;

        logger.info("Setting to " + dsp_volume + "db");

        dsp_volume = Math.pow(10.0, dsp_volume/20.0);

        String data = this.makeParameter(20396, dsp_volume);

        try {
            this.sendMessage(data);
            this.sendMessage("\r");
        }
        catch (IOException e)
        {
            e.printStackTrace();
        }
    }

    String getInput() {
        return input;
    }

    void setInput(String input) {
        this.input = input;
    }

    String makeParameter(Integer reg, double val)
    {
        String data = "";

        data = data + Integer.toHexString((reg >> 8) & 0x000000FF);
        data = data + Integer.toHexString(reg & 0x000000FF);

        long val_824 = this.convertTo824(val);

        data = data + String.format("%02X", (byte)((val_824 >> 24) & 0x000000FF));
        data = data + String.format("%02X", (byte)((val_824 >> 16) & 0x000000FF));
        data = data + String.format("%02X", (byte)((val_824 >> 8) & 0x000000FF));
        data = data + String.format("%02X", (byte)(val_824 & 0x000000FF));

        logger.info(data);

        return data;
    }

    // https://wiki.analog.com/resources/tools-software/sigmastudio/usingsigmastudio/numericformats
    long convertTo824( double val )
    {
        double fractpart;
        short intpart;

        long ret;

        intpart = (short) Math.floor( val );
        fractpart = val - intpart;

        ret = ((intpart << 24) & 0xff000000)
                + ((short)(fractpart * 16777216.f) & 0x00ffffff);

        return ret;
    }

    @Override
    public void processData(String line) {
        logger.info(line);
    }
}
