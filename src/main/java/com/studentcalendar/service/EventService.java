package com.studentcalendar.service;

import java.time.LocalDateTime;
import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import com.studentcalendar.exception.ResourceNotFoundException;
import com.studentcalendar.model.Event;
import com.studentcalendar.repository.EventRepository;

@Service
public class EventService {

    private final EventRepository eventRepository;

    @Autowired
    public EventService(EventRepository eventRepository) {
        this.eventRepository = eventRepository;
    }

    @Transactional(readOnly = true)
    public boolean checkForTimeConflicts(Event event) {
        return eventRepository.findOverlappingEvents(
            event.getUserId(),
            event.getStartTime(),
            event.getEndTime()
        ).size() > 0;
    }

    @Transactional
    public Event createEvent(Event event, String userId) {
        event.setUserId(userId);
        event.setCreatedAt(LocalDateTime.now());
        event.setUpdatedAt(LocalDateTime.now());
        return eventRepository.save(event);
    }

    @Transactional(readOnly = true)
    public List<Event> getEventsByUser(String userId) {
        return eventRepository.findByUserId(userId);
    }

    @Transactional
    public Event updateEvent(String id, Event eventDetails) {
        Event event = eventRepository.findById(id)
            .orElseThrow(() -> new ResourceNotFoundException("Event not found with id: " + id));
        
        event.setTitle(eventDetails.getTitle());
        event.setStartTime(eventDetails.getStartTime());
        event.setEndTime(eventDetails.getEndTime());
        event.setDescription(eventDetails.getDescription());
        event.setPriority(eventDetails.getPriority());
        event.setRecurrence(eventDetails.getRecurrence());
        event.setConflictFlag(eventDetails.isConflictFlag());
        event.setUpdatedAt(LocalDateTime.now());
        
        return eventRepository.save(event);
    }

    @Transactional
    public void deleteEvent(String id) {
        if (!eventRepository.existsById(id)) {
            throw new ResourceNotFoundException("Event not found with id: " + id);
        }
        eventRepository.deleteById(id);
    }
}