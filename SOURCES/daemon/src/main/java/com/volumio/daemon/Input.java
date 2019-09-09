package com.volumio.daemon;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

@Component
public class Input {
    @Autowired
    Dsp dsp;

    public String getInput() {
        return dsp.getInput();
    }

    public void setInput(String input) {
        dsp.setInput(input);
    }
}
