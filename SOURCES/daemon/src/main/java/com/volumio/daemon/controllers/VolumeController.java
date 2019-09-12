package com.volumio.daemon.controllers;


import com.volumio.daemon.Volume;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Controller;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.*;

import javax.validation.constraints.Max;
import javax.validation.constraints.Min;
import javax.validation.constraints.NotBlank;

@Controller
@Validated
public class VolumeController {

    @Autowired
    Volume volume;

    @GetMapping("/volume")
    @ResponseBody
    public int getVolume() {
        return this.volume.getVolume();
    }

    @PutMapping("/volume/{vol}")
    @ResponseBody
    void putVolume(@PathVariable(value="vol") @Min(-120) @Max(0) Integer volume) {
        this.volume.setVolume(volume);
    }
}
