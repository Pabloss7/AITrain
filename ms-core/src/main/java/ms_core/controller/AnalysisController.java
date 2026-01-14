package ms_core.controller;

import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import ms_core.DTO.AnalysisRequestDTO;
import ms_core.DTO.AnalysisResponseDTO;
import ms_core.DTO.JobStatusResponseDTO;
import ms_core.models.Job;
import ms_core.models.JobStatus.JobStatusEnum;
import ms_core.service.AIService;
import ms_core.service.AnalysisService;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import tools.jackson.databind.JsonNode;

import java.util.UUID;

@RestController
@RequestMapping("/analysis")
@RequiredArgsConstructor
public class AnalysisController {

    private final AnalysisService analysisService;
    private final AIService aiService;
    //TODO: FIX OVERWRITTING BEFORE CREATING
    @PostMapping
    @ResponseStatus(HttpStatus.ACCEPTED)
    public AnalysisResponseDTO  createAnalysis(@Valid @RequestBody AnalysisRequestDTO request){
        Job job = analysisService.createJob(
                request.getSummonerName(),
                request.getTagLine()
        );

        return new AnalysisResponseDTO(job.getJobId(),job.getStatus());
    }
    @GetMapping("/{jobId}/status")
    public ResponseEntity<?> getStatus(@PathVariable("jobId") UUID jobId){
        Job job = analysisService.getJob(jobId);
        if(!job.getStatus().equals(JobStatusEnum.COMPLETED)){
            return ResponseEntity.status(HttpStatus.ACCEPTED).build();
        }
        JsonNode recomms = aiService.getReccoms(jobId);
        return ResponseEntity.status(HttpStatus.OK).body(recomms);
    }

    @PatchMapping("/{jobId}/running")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    public void markJobAsRunning(@PathVariable("jobId") UUID jobId){
        System.out.println("Marking job as running");
        analysisService.updateJob(jobId, JobStatusEnum.RUNNING);
    }

    @PatchMapping("/{jobId}/completed")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    public void markJobAsCompleted(@PathVariable("jobId") UUID jobId){
        System.out.println("Marking job as completed");
        analysisService.updateJob(jobId, JobStatusEnum.COMPLETED);
    }

    @PatchMapping("/{jobId}/error")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    public void markJobAsError(@PathVariable("jobId") UUID jobId){
        analysisService.updateJob(jobId, JobStatusEnum.ERROR);
    }
}
