package com.studentcalendar.service;

import com.studentcalendar.model.Event;
import com.studentcalendar.repository.EventRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;
import java.util.List;

@Service
public class EventService {

    @Autowired
    private EventRepository eventRepository;

    public Event createEvent(Event event) {
        checkForConflicts(event);
        return eventRepository.save(event);
    }

    public Event updateEvent(Event event) {
        checkForConflicts(event);
        return eventRepository.save(event);
    }

    private void checkForConflicts(Event event) {
        List<Event> overlappingEvents = eventRepository
            .findByUserIdAndTimeRange(event.getUserId(), event.getStartTime(), event.getEndTime());
        
        if(!overlappingEvents.isEmpty()) {
            event.setConflictFlag(true);
        }
    }
}