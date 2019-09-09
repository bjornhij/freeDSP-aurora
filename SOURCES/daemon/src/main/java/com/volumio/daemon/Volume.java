package com.volumio.daemon;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

@Component
public class Volume {
    @Autowired
    Dsp dsp;

    public int getVolume() {
        return dsp.getVolume();
    }

    public void setVolume(int volume) {
        dsp.setVolume(volume);
    }
}
