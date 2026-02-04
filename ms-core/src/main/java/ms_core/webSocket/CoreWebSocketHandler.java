package ms_core.webSocket;

import ms_core.DTO.AnalysisRequestDTO;
import ms_core.DTO.WSMessage;
import ms_core.models.Job;
import ms_core.service.AnalysisService;
import org.springframework.stereotype.Component;
import org.springframework.web.socket.CloseStatus;
import org.springframework.web.socket.TextMessage;
import org.springframework.web.socket.WebSocketSession;
import org.springframework.web.socket.handler.TextWebSocketHandler;
import tools.jackson.databind.ObjectMapper;

import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;

@Component
public class CoreWebSocketHandler extends TextWebSocketHandler {

        private final AnalysisService analysisService;
        private final ObjectMapper objectMapper = new ObjectMapper();
        private final Map<String, WebSocketSession> sessions = new ConcurrentHashMap<>();

        public CoreWebSocketHandler(AnalysisService analysisService) {
                this.analysisService = analysisService;
        }

        @Override
        public void afterConnectionClosed(WebSocketSession session, CloseStatus status) throws Exception {
                // Optional: cleanup execution if needed, but for now we rely on the Map
                // overwrites or checks
        }

        @Override
        protected void handleTextMessage(
                        WebSocketSession session,
                        TextMessage message) throws Exception {
                WSMessage wsMessage = objectMapper.readValue(message.getPayload(), WSMessage.class);

                if ("recom_request".equals(wsMessage.getType())) {
                        AnalysisRequestDTO payload = objectMapper.convertValue(wsMessage.getPayload(),
                                        AnalysisRequestDTO.class);

                        Job job = analysisService.createJob(
                                        payload.getSummonerName(),
                                        payload.getTagLine());

                        sessions.put(job.getJobId().toString(), session);

                        session.sendMessage(new TextMessage(
                                        objectMapper.writeValueAsString(
                                                        WSMessage.of(
                                                                        "job_created",
                                                                        Map.of("jobId", job.getJobId())))));
                }
        }

        public void sendRecommendation(String jobId, Object recommendation) {
                WebSocketSession session = sessions.get(jobId);
                if (session != null && session.isOpen()) {
                        try {
                                session.sendMessage(new TextMessage(
                                                objectMapper.writeValueAsString(
                                                                WSMessage.of("recommendation", recommendation))));
                                // Optional: Remove from map after success?
                                sessions.remove(jobId);
                                session.close();
                        } catch (Exception e) {
                                e.printStackTrace();
                        }
                }
        }
}
