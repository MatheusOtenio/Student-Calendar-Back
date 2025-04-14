package com.studentcalendar.repositories;

import com.studentcalendar.entities.Event;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import java.time.Instant;
import java.util.List;

public interface EventRepository extends JpaRepository<Event, String> {

    @Query(value = "SELECT * FROM events WHERE user_id = :userId AND 
        tsrange(start_time, end_time) && tsrange(:start, :end)",
        nativeQuery = true)
    List<Event> findOverlappingEvents(
        @Param("userId") String userId,
        @Param("start") Instant start,
        @Param("end") Instant end
    );

    List<Event> findByUserId(String userId);
}