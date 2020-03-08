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

        //double dsp_volume = Math.log10(volume/100.0) * 20.0;
        double dsp_volume = -80 + (volume * 0.8);

        logger.info("Setting to " + dsp_volume + "db");

        this.sendData("/mvol", Double.toString((int)(dsp_volume)));
    }

    public void reset()
    {
        this.sendData("/reset", "true");
    }

    void sendData(String handler, String data)
    {
        String message = handler + "|" + data;

        logger.info("Sending: " + message);

        try {
            this.sendMessage(message);
            this.sendMessage("\n");
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

        switch(input)
        {
            case "usb":

                // input
                // {"idx":0,"sel":"0x00010000"}
                // {"idx":1,"sel":"0x00010001"}

                this.sendData("/input", "idx|0|sel|0x00010000");
                this.sendData("/input", "idx|1|sel|0x00010001");


                break;
            case "analog_1":

                // input
                // {"idx":0,"sel":"0x00000000"}
                // {"idx":1,"sel":"0x00000001"}

                this.sendData("/input", "idx|0|sel|0x00000000");
                this.sendData("/input", "idx|1|sel|0x00000001");

                break;
            case "analog_2":

                // input
                // {"idx":0,"sel":"0x00000002"}
                // {"idx":1,"sel":"0x00000003"}

                this.sendData("/input", "idx|0|sel|0x00000002");
                this.sendData("/input", "idx|1|sel|0x00000003");

                break;
            case "analog_3":

                // input
                // {"idx":0,"sel":"0x00000004"}
                // {"idx":1,"sel":"0x00000005"}

                this.sendData("/input", "idx|0|sel|0x00000004");
                this.sendData("/input", "idx|1|sel|0x00000005");

                break;
            case "analog_4":

                // input
                // {"idx":0,"sel":"0x00000006"}
                // {"idx":1,"sel":"0x00000007"}

                this.sendData("/input", "idx|0|sel|0x00000006");
                this.sendData("/input", "idx|1|sel|0x00000007");

                break;
            case "optical_1":

                // addoncfg
                // {"len":3,"i2c":["0x82","0x01","0x00"]}
                this.sendData("/addoncfg", "0x82|0x01|0x00");

                // input
                // {"idx":0,"sel":"0x00040000"}
                // {"idx":1,"sel":"0x00040001"}

                this.sendData("/input", "idx|0|sel|0x00040000");
                this.sendData("/input", "idx|1|sel|0x00040001");

                break;
            case "optical_2":

                // addoncfg
                // {"len":3,"i2c":["0x82","0x01","0x01"]}
                this.sendData("/addoncfg", "0x82|0x01|0x01");

                // input
                // {"idx":0,"sel":"0x00040000"}
                // {"idx":1,"sel":"0x00040001"}

                this.sendData("/input", "idx|0|sel|0x00040000");
                this.sendData("/input", "idx|1|sel|0x00040001");

                break;
            case "optical_3":

                // addoncfg
                // {"len":3,"i2c":["0x82","0x01","0x02"]}
                this.sendData("/addoncfg", "0x82|0x01|0x02");


                // input
                // {"idx":0,"sel":"0x00040000"}
                // {"idx":1,"sel":"0x00040001"}

                this.sendData("/input", "idx|0|sel|0x00040000");
                this.sendData("/input", "idx|1|sel|0x00040001");

                break;
            case "optical_4":

                // addoncfg
                // {"len":3,"i2c":["0x82","0x01","0x03"]}
                this.sendData("/addoncfg", "0x82|0x01|0x03");

                // input
                // {"idx":0,"sel":"0x00040000"}
                // {"idx":1,"sel":"0x00040001"}

                this.sendData("/input", "idx|0|sel|0x00040000");
                this.sendData("/input", "idx|1|sel|0x00040001");

                break;

        }

    }

    String makeParameter(Integer reg, double val)
    {
        String data = "";

        data = data + Integer.toHexString((reg >> 8) & 0x000000FF);
        data = data + Integer.toHexString(reg & 0x000000FF);

        long val_824 = this.convertTo824(val);

        logger.info(String.format("%32s", Long.toBinaryString(val_824)).replace(' ', '0'));

        data = data + String.format("%02X", (byte)((val_824 >> 24) & 0x000000FF));
        data = data + String.format("%02X", (byte)((val_824 >> 16) & 0x000000FF));
        data = data + String.format("%02X", (byte)((val_824 >> 8) & 0x000000FF));
        data = data + String.format("%02X", (byte)(val_824 & 0x000000FF));

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

        logger.info("intpart=" + intpart);
        logger.info("fractpart=" + fractpart);


        ret = ((intpart << 24) & 0xff000000)
                + ((long)(fractpart * 16777216.f) & 0x00ffffff);

        return ret;
    }

    @Override
    public void processData(String line) {
        logger.info(line);
    }
}
