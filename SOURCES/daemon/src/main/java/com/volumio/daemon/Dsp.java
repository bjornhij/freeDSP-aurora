package com.volumio.daemon;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.core.env.Environment;
import org.springframework.stereotype.Component;

@Component
public class Dsp {

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
    }

    String getInput() {
        return input;
    }

    void setInput(String input) {
        this.input = input;
    }
}
