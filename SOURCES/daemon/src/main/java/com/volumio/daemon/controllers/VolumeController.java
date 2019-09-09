package com.volumio.daemon.controllers;


import com.volumio.daemon.Volume;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.*;

@Controller
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
    void putVolume(@PathVariable(value="vol") int volume) {
        this.volume.setVolume(volume);
    }
}
