package com.volumio.daemon.controllers;

import com.volumio.daemon.Input;
import com.volumio.daemon.State;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.ResponseBody;

@Controller
@Validated
public class StateController {
    @Autowired
    State state;

    @GetMapping("/state")
    @ResponseBody
    public String getInput() {
        return this.state.getState();
    }

    @PutMapping("/state/{state}")
    @ResponseBody
    void putInput(@PathVariable(value="state") String state) {
        this.state.setState(state);
    }
}
