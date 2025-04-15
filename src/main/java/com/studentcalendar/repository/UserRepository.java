package com.studentcalendar.repository;

import java.util.Optional;

import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.stereotype.Repository;

import com.studentcalendar.model.User;

@Repository
public interface UserRepository extends MongoRepository<User, String> {
    // Este método estava faltando ou não tinha o nome correto
    Optional<User> findByUsername(String username);
}