package com.studentcalendar.model;

import java.time.LocalDateTime;

import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Document(collection = "events")
@Data
@NoArgsConstructor
@AllArgsConstructor
public class Event {
    @Id
    private String id;
    
    private String userId;
    
    private String title;
    
    private LocalDateTime startTime;
    
    private LocalDateTime endTime;
    
    private String description;
    
    private Integer priority = 3;
    
    private String recurrence;
    
    private boolean conflictFlag;
    
    private LocalDateTime createdAt = LocalDateTime.now();
    
    private LocalDateTime updatedAt = LocalDateTime.now();
    
    public String getRecurrence() {
        return recurrence;
    }
    
    public void setRecurrence(String recurrence) {
        this.recurrence = recurrence;
    }
    
    public boolean isConflictFlag() {
        return conflictFlag;
    }
    
    public void setConflictFlag(boolean conflictFlag) {
        this.conflictFlag = conflictFlag;
    }
}