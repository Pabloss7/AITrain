package data_collector.controller;

import data_collector.DTO.AnalyzeMatchRequestDTO;
import data_collector.service.RiotAPIService;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/data-collector")

public class RiotAPIController {

    private RiotAPIService service = new RiotAPIService();


    @PostMapping("/analyze-match")
    @ResponseStatus(HttpStatus.OK)
    public String analyzeMatch(@RequestBody AnalyzeMatchRequestDTO request){
        String match = service.getSingleMatch(request.getSummonerName(),request.getTagLine(), request.getJobId());
        return "analysis in process for match:\n"+match;
    }
}
