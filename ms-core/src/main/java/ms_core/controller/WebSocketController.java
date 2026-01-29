package ms_core.controller;

import ms_core.DTO.AnalysisRequestDTO;
import ms_core.service.AnalysisService;
import org.springframework.messaging.handler.annotation.MessageMapping;
import org.springframework.stereotype.Controller;

import java.util.UUID;

@Controller
public class WebSocketController {

    private final AnalysisService analysisService;

    public WebSocketController(AnalysisService analysisService) {
        this.analysisService = analysisService;
    }

    @MessageMapping("/analyze")
    public void analyze(AnalysisRequestDTO request){
        analysisService.createJob(
                request.getSummonerName(),
                request.getTagLine()
        );
    }
}
