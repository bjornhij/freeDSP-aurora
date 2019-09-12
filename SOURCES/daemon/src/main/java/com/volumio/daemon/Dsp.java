package com.volumio.daemon;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.core.env.Environment;
import org.springframework.stereotype.Component;

@Component
public class Dsp {

    Logger logger = LoggerFactory.getLogger(Dsp.class);

    @Autowired
    private Environment env;

    @Value("${volumiodaemon.initial_volume:-120}")
    private int volume;

    @Value("${volumiodaemon.initial_input}")
    private String input;

    int getVolume() {
        return volume;
    }

    void setVolume(int volume) {

        this.volume = volume;

        double dsp_volume = Math.pow(10.0, volume/20.0);

        logger.info(Double.toString(dsp_volume));

        // 4fac00012cd7
        String data = this.makeParameter(20396, dsp_volume);

        logger.info(data);
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

        logger.info(data);

        data = data + String.format("%02X", (byte)((val_824 >> 16) & 0x000000FF));

        logger.info(data);

        data = data + String.format("%02X", (byte)((val_824 >> 8) & 0x000000FF));

        logger.info(data);

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

        logger.info(Long.toBinaryString(intpart));

        logger.info(Float.toString(intpart)); logger.info(Double.toString(fractpart));

        ret = ((intpart << 24) & 0xff000000)
                + ((short)(fractpart * 16777216.f) & 0x00ffffff);

        logger.info(Long.toBinaryString(ret));

        return ret;
    }
}
