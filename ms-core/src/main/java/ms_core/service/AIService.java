package ms_core.service;

import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;
import tools.jackson.databind.JsonNode;

import java.util.UUID;

@Service
public class AIService {

    private final RestTemplate restTemplate;
    public AIService(RestTemplate restTemplate) {
        this.restTemplate = restTemplate;
    }

    public JsonNode getReccoms(UUID jobId){
        return restTemplate.getForObject("http://ms-ai:5000/recommendations/"+jobId.toString(), JsonNode.class);
    }
}
