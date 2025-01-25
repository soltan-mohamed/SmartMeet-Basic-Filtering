package tn.esprit.aialgorithme.service;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.core.ParameterizedTypeReference;
import org.springframework.stereotype.Service;
import org.springframework.web.reactive.function.client.WebClient;
import tn.esprit.aialgorithme.model.User;
import tn.esprit.aialgorithme.repository.UserRepository;

import java.time.Duration;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

@Service
public class AIServiceClient {
    private final WebClient webClient;


    @Autowired
    public AIServiceClient(@Qualifier("aiWebClient") WebClient webClient) {
        this.webClient = webClient;
    }

    public List<User> findMatches(User currentUser, List<User> otherUsers) {
        // Example: Return users with matching interests
        return otherUsers.stream()
                .filter(user -> !user.getId().equals(currentUser.getId()))
                .filter(user -> user.getInterests().stream()
                        .anyMatch(interest -> currentUser.getInterests().contains(interest))
                )
                .collect(Collectors.toList());
    }

    private Map<String, Object> convertUserToMap(User user) {
        return Map.of(
                "id", user.getId(),
                "name", user.getName(),
                "interests", user.getInterests()
        );
    }
}
