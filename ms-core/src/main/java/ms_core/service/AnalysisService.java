package ms_core.service;

import lombok.RequiredArgsConstructor;
import ms_core.DTO.DataAnalysisRequest;
import ms_core.models.Job;
import ms_core.models.JobStatus.JobStatusEnum;
import ms_core.repositories.AnalysisJobRepo;
import org.springframework.stereotype.Service;

import java.time.Instant;
import java.util.UUID;

@Service
@RequiredArgsConstructor
public class AnalysisService {

    private final AnalysisJobRepo repository;
    private final DataService dataService;
    public Job createJob(String summonerName, String tagLine){
        Job job = Job.builder()
                .jobId(UUID.randomUUID())
                .summonerName(summonerName)
                .tagLine(tagLine)
                .status(JobStatusEnum.PENDING)
                .createdAt(Instant.now())
                .build();

        DataAnalysisRequest body =  DataAnalysisRequest.builder()
                .jobId(job.getJobId())
                .summonerName(summonerName)
                .tagLine(tagLine)
                .build();
        System.out.println("Sending job: \n"+job);
        Job savedJob = repository.save(job);
        dataService.startAnalysis(body);
        return savedJob;
    }

    public Job getJob(UUID jobId){
        return repository.findById(jobId)
                .orElseThrow(() -> new RuntimeException("Job not found"));
    }

    public void updateJob(UUID jobId, JobStatusEnum status){
        Job job = getJob(jobId);
        job.setStatus(status);
        job.setUpdatedAt(Instant.now());
        repository.save(job);
    }
}
