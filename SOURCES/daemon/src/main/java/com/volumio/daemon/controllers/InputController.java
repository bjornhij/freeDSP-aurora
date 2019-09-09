package com.volumio.daemon.controllers;

import com.volumio.daemon.Input;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.ResponseBody;

@Controller
@Validated
public class InputController {
    @Autowired
    Input input;

    @GetMapping("/input")
    @ResponseBody
    public String getInput() {
        return this.input.getInput();
    }

    @PutMapping("/input/{input}")
    @ResponseBody
    void putInput(@PathVariable(value="input") String input) {
        this.input.setInput(input);
    }
}
