package com.volumio.daemon;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

@Component
public class State {
    @Autowired
    Hypex hypex;

    public String getState() {
        return hypex.getState();
    }

    public void setState(String state) {
        hypex.setState(state);
    }
}
