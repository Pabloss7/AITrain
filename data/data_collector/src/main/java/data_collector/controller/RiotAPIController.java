package data_collector.controller;

import data_collector.DTO.AnalyzeMatchRequestDTO;
import data_collector.DTO.MatchAISenderDTO;
import data_collector.service.RiotAPIService;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/data-collector")

public class RiotAPIController {

    private final RiotAPIService service;

    public RiotAPIController(RiotAPIService service) {
        this.service = service;
    }


    @PostMapping("/analyze-match")
    @ResponseStatus(HttpStatus.OK)
    public MatchAISenderDTO analyzeMatch(@RequestBody AnalyzeMatchRequestDTO request){
        return service.getSingleMatch(request.getSummonerName(),request.getTagLine(), request.getJobId());
    }
}
