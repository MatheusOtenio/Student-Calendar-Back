package com.studentcalendar.model;

import java.util.Collection;
import java.util.List;
import java.util.Set;

import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.DBRef;
import org.springframework.data.mongodb.core.mapping.Document;
import org.springframework.security.core.GrantedAuthority;
import org.springframework.security.core.authority.SimpleGrantedAuthority;
import org.springframework.security.core.userdetails.UserDetails;

@Document(collection = "users")
public class User implements UserDetails {
    @Id
    private String id;
    
    private String username;
    
    private String password;
    
    @DBRef
    private Set<Event> events;

    // UserDetails interface methods
    @Override
    public Collection<? extends GrantedAuthority> getAuthorities() {
        return List.of(new SimpleGrantedAuthority("ROLE_USER"));
    }

    // Getters and setters
    public String getId() { return id; }
    public String getUsername() { return username; }
    public String getPassword() { return password; }
    public Set<Event> getEvents() { return events; }

    public void setUsername(String username) { this.username = username; }
    public void setPassword(String password) { this.password = password; }
    public void setEvents(Set<Event> events) { this.events = events; }

    // Security interface methods
    @Override
    public boolean isAccountNonExpired() { return true; }
    @Override
    public boolean isAccountNonLocked() { return true; }
    @Override
    public boolean isCredentialsNonExpired() { return true; }
    @Override
    public boolean isEnabled() { return true; }
}