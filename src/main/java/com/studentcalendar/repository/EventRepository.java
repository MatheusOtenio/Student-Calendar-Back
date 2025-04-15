package com.studentcalendar.repository;

import java.time.LocalDateTime;
import java.util.List;

import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.data.mongodb.repository.Query;

import com.studentcalendar.model.Event;

public interface EventRepository extends MongoRepository<Event, String> {

    @Query("{ 'userId': ?0, $or: [ { 'startTime': { $gte: ?1, $lte: ?2 } }, { 'endTime': { $gte: ?1, $lte: ?2 } } ] }")
    List<Event> findOverlappingEvents(String userId, LocalDateTime start, LocalDateTime end);

    List<Event> findByUserId(String userId);
}