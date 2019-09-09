package com.volumio.daemon;

import org.springframework.stereotype.Component;

@Component
public class Dsp {

    private int volume;

    int getVolume() {
        return volume;
    }

    void setVolume(int volume) {
        this.volume = volume;
    }
}
