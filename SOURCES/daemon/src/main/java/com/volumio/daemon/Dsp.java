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

        double dsp_volume = Math.log(volume / 200.0) * 20;

        logger.info("Setting to " + dsp_volume + "db");

        dsp_volume = Math.pow(10.0, dsp_volume/20.0);

        logger.info("Setting to " + dsp_volume + "??");


        String data = this.makeParameter(0x4fb9, dsp_volume);

        logger.info("Calculated: " + data);

        this.sendData("D" + data);
    }

    void sendData(String data)
    {
        logger.info("Sending: " + data);


        try {
            this.sendMessage(data);
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


        this.sendData("I" + "200123");


        switch(input)
        {
            case "usb":
                // channel 1
                //
                // I200123
                // D4fe100000000
                // D4fec00000001
                // I200122
                //
                this.sendData("D" + "4fe100000000");
                this.sendData("D" + "4fec00000001");

                // channel 2
                // I200123
                // D4fdd00000001
                // D4feb00000001
                // I200122

                this.sendData("D" + "4fdd00000001");
                this.sendData("D" + "4feb00000001");

                break;
            case "analog_1":

                // channel 1
                // I200123
                // D4fe000000000
                // D4fec00000000
                // I200122

                this.sendData("D" + "4fe000000000");
                this.sendData("D" + "4fec00000000");

                // channel 2
                // channel 1
                // I200123
                // D4fde00000001
                // D4feb00000000
                // I200122

                this.sendData("D" + "4fde00000001");
                this.sendData("D" + "4feb00000000");

                break;
            case "analog_2":

                // channel 1
                // 4fe000000002
                // 4fec00000000

                this.sendData("D" + "4fe000000002");
                this.sendData("D" + "4fec00000000");

                // channel 2
                // 4fde00000003
                // 4feb00000000

                this.sendData("D" + "4fde00000003");
                this.sendData("D" + "4feb00000000");

                break;
            case "analog_3":

                // channel 1
                // 4fe000000004
                // 4fec00000000

                this.sendData("D" + "4fe000000004");
                this.sendData("D" + "4fec00000000");

                // channel 2
                // 4fde00000005
                // 4feb00000000

                this.sendData("D" + "4fde00000005");
                this.sendData("D" + "4feb00000000");

                break;
            case "analog_4":

                // channel 1
                // 4fe000000006
                // 4fec00000000

                this.sendData("D" + "4fe000000006");
                this.sendData("D" + "4fec00000000");

                // channel 2
                // 4fde00000007
                // 4feb00000000

                this.sendData("D" + "4fde00000007");
                this.sendData("D" + "4feb00000000");

                break;
            case "optical_1":

                this.sendData("I" + "820100");

                // channel 1
                // 4fe400000000
                // 4fec00000004

                this.sendData("D" + "4fe400000000");
                this.sendData("D" + "4fec00000004");

                // channel 2
                // 4fdc00000001
                // 4feb00000004

                this.sendData("D" + "4fdc00000001");
                this.sendData("D" + "4feb00000004");

                break;
            case "optical_2":

                this.sendData("I" + "820101");

                // channel 1
                // 4fe400000000
                // 4fec00000004

                this.sendData("D" + "4fe400000000");
                this.sendData("D" + "4fec00000004");

                // channel 2
                // 4fdc00000001
                // 4feb00000004

                this.sendData("D" + "4fdc00000001");
                this.sendData("D" + "4feb00000004");

                break;
            case "optical_3":

                this.sendData("I" + "820102");

                // channel 1
                // 4fe400000000
                // 4fec00000004

                this.sendData("D" + "4fe400000000");
                this.sendData("D" + "4fec00000004");

                // channel 2
                // 4fdc00000001
                // 4feb00000004

                this.sendData("D" + "4fdc00000001");
                this.sendData("D" + "4feb00000004");

                break;
            case "optical_4":

                this.sendData("I" + "820103");

                // channel 1
                // 4fe400000000
                // 4fec00000004

                this.sendData("D" + "4fe400000000");
                this.sendData("D" + "4fec00000004");

                // channel 2
                // 4fdc00000001
                // 4feb00000004

                this.sendData("D" + "4fdc00000001");
                this.sendData("D" + "4feb00000004");

                break;

        }

        this.sendData("I" + "200122");
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
