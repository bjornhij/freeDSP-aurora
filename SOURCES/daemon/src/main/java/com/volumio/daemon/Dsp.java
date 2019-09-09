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

    @Value("${volumiodaemon.initial_volume:10}")
    private int volume;

    @Value("${volumiodaemon.initial_input}")
    private String input;

    int getVolume() {
        return volume;
    }

    void setVolume(int volume) {

        this.volume = volume;

        // 4fac00012cd7
        String data = this.makeParameter(20396, volume);

        logger.info(data);
    }

    String getInput() {
        return input;
    }

    void setInput(String input) {
        this.input = input;
    }

    String makeParameter(Integer reg, float val)
    {
        String data = "";

        data = data + Integer.toHexString((reg >> 8) & 0x000000FF);
        data = data + Integer.toHexString(reg & 0x000000FF);

        Integer val_824 = this.convertTo824(val);

        data = data + Integer.toHexString((val_824 >> 24) & 0x000000FF);
        data = data + Integer.toHexString((val_824 >> 16) & 0x000000FF);
        data = data + Integer.toHexString((val_824 >> 8) & 0x000000FF);
        data = data + Integer.toHexString(val_824 & 0x000000FF);

        return data;
    }

    // https://wiki.analog.com/resources/tools-software/sigmastudio/usingsigmastudio/numericformats
    Integer convertTo824( float val )
    {
        float fractpart;
        int intpart;

        int ret;

        intpart = (int) Math.floor( val );
        fractpart = val - intpart;

        ret = ((intpart << 24) & 0xff000000)
                + ((int)(fractpart * 16777216.f) & 0x00ffffff);

        return ret;
    }
}
