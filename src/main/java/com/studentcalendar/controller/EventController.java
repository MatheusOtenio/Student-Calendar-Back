package com.studentcalendar.controller;

import com.studentcalendar.model.Event;
import com.studentcalendar.service.EventService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/events")
public class EventController {

    private final EventRepository eventRepository;

    public EventController(EventRepository eventRepository) {
        this.eventRepository = eventRepository;
    }

    @GetMapping
    @PreAuthorize("hasRole('USER')")
    public ResponseEntity<List<CalendarEvent>> getAllEvents() {
        return ResponseEntity.ok(eventRepository.findAll());
    }

    @PostMapping
    @PreAuthorize("hasRole('USER')")
    public ResponseEntity<CalendarEvent> createEvent(@RequestBody CalendarEvent event) {
        event.setUser(SecurityUtils.getCurrentUser());
        return ResponseEntity.ok(eventRepository.save(event));
    }

    @PutMapping("/{id}")
    @PreAuthorize("hasRole('USER')")
    public ResponseEntity<CalendarEvent> updateEvent(@PathVariable Long id, @RequestBody CalendarEvent event) {
        return eventRepository.findByIdAndUser(id, SecurityUtils.getCurrentUser())
            .map(existingEvent -> {
                existingEvent.setTitle(event.getTitle());
                existingEvent.setStart(event.getStart());
                existingEvent.setEnd(event.getEnd());
                existingEvent.setDescription(event.getDescription());
                return ResponseEntity.ok(eventRepository.save(existingEvent));
            })
            .orElseGet(() -> ResponseEntity.notFound().build());
    }

    @DeleteMapping("/{id}")
    @PreAuthorize("hasRole('USER')")
    public ResponseEntity<Void> deleteEvent(@PathVariable Long id) {
        eventRepository.deleteByIdAndUser(id, SecurityUtils.getCurrentUser());
        return ResponseEntity.noContent().build();
    }
}