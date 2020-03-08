package com.volumio.daemon.controllers;


import com.volumio.daemon.Dsp;
import com.volumio.daemon.Hypex;
import com.volumio.daemon.Volume;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.ResponseBody;

import javax.validation.constraints.Pattern;

@Controller
@Validated
public class ResetdspController {

    @Autowired
    Dsp dsp;
    @Autowired
    Hypex hypex;

    @GetMapping("/resetdsp")
    @ResponseBody
    public String resetDsp() {
        hypex.setState("off");
        dsp.reset();
        return "OK";
    }
}
