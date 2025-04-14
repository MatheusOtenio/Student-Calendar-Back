package com.studentcalendar.entities;

import jakarta.persistence.*;
import lombok.Data;
import org.hibernate.annotations.CreationTimestamp;
import org.hibernate.annotations.UpdateTimestamp;

import java.time.Instant;
import java.time.ZoneId;

@Entity
@Table(name = "events")
@Data
public class Event {
    @Id
    @GeneratedValue(generator = "uuid2")
    private String id;
    
    @Column(nullable = false)
    private String title;
    
    @Column(name = "start_time", nullable = false)
    private Instant startTime;
    
    @Column(name = "end_time", nullable = false)
    private Instant endTime;
    
    private String description;
    
    @Column(nullable = false)
    private Integer priority = 3;
    
    @Column(name = "recurrence_rule")
    private String recurrenceRule;
    
    @Column(name = "time_zone", nullable = false)
    private String timeZone = ZoneId.systemDefault().toString();
    
    @Column(name = "user_id", nullable = false)
    private String userId;
    
    @CreationTimestamp
    @Column(name = "created_at", updatable = false)
    private Instant createdAt;

    @UpdateTimestamp
    @Column(name = "updated_at")
    private Instant updatedAt;
}