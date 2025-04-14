package com.studentcalendar.repository;

import com.studentcalendar.model.Event;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import java.time.LocalDateTime;
import java.util.List;

public interface EventRepository extends JpaRepository<CalendarEvent, Long> {
    List<CalendarEvent> findByUser(User user);
    
    Optional<CalendarEvent> findByIdAndUser(Long id, User user);
    
    void deleteByIdAndUser(Long id, User user);
    
    @Query("SELECT e FROM CalendarEvent e WHERE e.user = :user AND " +
           "(e.start BETWEEN :start AND :end OR e.end BETWEEN :start AND :end)")
    List<CalendarEvent> findBetweenDatesForUser(@Param("user") User user,
                                              @Param("start") LocalDateTime start,
                                              @Param("end") LocalDateTime end);
}