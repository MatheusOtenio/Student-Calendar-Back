package com.studentcalendar.controller;

import java.security.Principal;
import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
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

import com.studentcalendar.exception.ResourceNotFoundException;
import com.studentcalendar.model.Event;
import com.studentcalendar.services.EventService;

@RestController
@RequestMapping("/api/events")
public class EventController {

    @Autowired
    private EventService eventService;

    @GetMapping("/user")
    @PreAuthorize("isAuthenticated()")
    public ResponseEntity<List<Event>> getUserEvents(Principal principal) {
        List<Event> events = eventService.getEventsByUser(principal.getName());
        return new ResponseEntity<>(events, HttpStatus.OK);
    }

    @PostMapping("/check-conflict")
    @PreAuthorize("isAuthenticated()")
    public ResponseEntity<?> checkForConflicts(@RequestBody Event event) {
        boolean hasConflict = eventService.checkForTimeConflicts(event);
        return ResponseEntity.ok(hasConflict);
    }

    @PostMapping
    @PreAuthorize("isAuthenticated()")
    public ResponseEntity<Event> createEvent(@RequestBody Event event, Principal principal) {
        Event createdEvent = eventService.createEvent(event, principal.getName());
        return new ResponseEntity<>(createdEvent, HttpStatus.CREATED);
    }

    @PutMapping("/{id}")
    @PreAuthorize("isAuthenticated()")
    public ResponseEntity<Event> updateEvent(@PathVariable String id, @RequestBody Event event) {
        try {
            Event updatedEvent = eventService.updateEvent(id, event);
            return new ResponseEntity<>(updatedEvent, HttpStatus.OK);
        } catch (ResourceNotFoundException e) {
            return new ResponseEntity<>(HttpStatus.NOT_FOUND);
        }
    }

    @DeleteMapping("/{id}")
    @PreAuthorize("isAuthenticated()")
    public ResponseEntity<Void> deleteEvent(@PathVariable String id) {
        try {
            eventService.deleteEvent(id);
            return ResponseEntity.noContent().build();
        } catch (ResourceNotFoundException e) {
            return new ResponseEntity<>(HttpStatus.NOT_FOUND);
        }
    }
}