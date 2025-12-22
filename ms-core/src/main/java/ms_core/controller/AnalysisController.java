package ms_core.controller;

import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import ms_core.DTO.AnalysisRequestDTO;
import ms_core.DTO.AnalysisResponseDTO;
import ms_core.DTO.JobStatusResponseDTO;
import ms_core.models.Job;
import ms_core.models.JobStatus.JobStatusEnum;
import ms_core.service.AnalysisService;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;

import java.util.UUID;

@RestController
@RequestMapping("/analysis")
@RequiredArgsConstructor
public class AnalysisController {

    private final AnalysisService analysisService;

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
    public JobStatusResponseDTO getStatus(@PathVariable("jobId") UUID jobId){
        Job job = analysisService.getJob(jobId);
        return new JobStatusResponseDTO(job.getJobId(),job.getStatus());
    }

    @PatchMapping("/{jobId}/running")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    public void markJobAsRunning(@PathVariable("jobId") UUID jobId){
        analysisService.updateJob(jobId, JobStatusEnum.RUNNING);
    }

    @PatchMapping("/{jobId/completed")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    public void markJobAsCompleted(@PathVariable("jobId") UUID jobId){
        analysisService.updateJob(jobId, JobStatusEnum.COMPLETED);
    }

    @PatchMapping("/{jobId/error")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    public void markJobAsError(@PathVariable("jobId") UUID jobId){
        analysisService.updateJob(jobId, JobStatusEnum.ERROR);
    }
}
