package com.studentcalendar.controllers;

import java.security.Principal;
import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.studentcalendar.model.Event;
import com.studentcalendar.services.EventService;

@RestController
@RequestMapping("/api/events")
public class EventController {

    @Autowired
    private EventService eventService;

    @GetMapping("/user")
    @PreAuthorize("isAuthenticated()")
    public List<Event> getUserEvents(Principal principal) {
        return eventService.getEventsByUser(principal.getName());
    }

    @PostMapping("/check-conflict")
    @PreAuthorize("isAuthenticated()")
    public ResponseEntity<?> checkForConflicts(@RequestBody Event event) {
        return ResponseEntity.ok(eventService.checkForTimeConflicts(event));
    }

    @PostMapping
    @PreAuthorize("isAuthenticated()")
    public Event createEvent(@RequestBody Event event, Principal principal) {
        return eventService.createEvent(event, principal.getName());
    }

    @PutMapping("/{id}")
    @PreAuthorize("isAuthenticated()")
    public Event updateEvent(@PathVariable String id, @RequestBody Event event) {
        return eventService.updateEvent(id, event);
    }

    @DeleteMapping("/{id}")
    @PreAuthorize("isAuthenticated()")
    public ResponseEntity<Void> deleteEvent(@PathVariable String id) {
        eventService.deleteEvent(id);
        return ResponseEntity.noContent().build();
    }
}