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

        public Job createJob(String summonerName, String tagLine) {
                Job job = Job.builder()
                                .jobId(UUID.randomUUID())
                                .summonerName(summonerName)
                                .tagLine(tagLine)
                                .status(JobStatusEnum.PENDING)
                                .createdAt(Instant.now())
                                .build();
                Job savedJob = repository.save(job);

                // STOMP notification removed. WebSocket notification now handled by
                // CoreWebSocketHandler in Controller or Handler itself.
                // Actually, CoreWebSocketHandler sends 'job_created' immediately upon request
                // in the handler.
                // But what if createJob is called from HTTP? The Controller calls createJob.
                // The WebSocket Handler also calls createJob.
                // If called from WebSocket Handler, it sends the response there.
                // If called from HTTP (not used in this flow anymore properly, but exists), it
                // returns Job.

                DataAnalysisRequest body = DataAnalysisRequest.builder()
                                .jobId(job.getJobId())
                                .summonerName(summonerName)
                                .tagLine(tagLine)
                                .build();
                System.out.println("Sending job: \n" + job);

                dataService.startAnalysis(body);
                return savedJob;
        }

        public Job getJob(UUID jobId) {
                return repository.findById(jobId)
                                .orElseThrow(() -> new RuntimeException("Job not found"));
        }

        public void updateJob(UUID jobId, JobStatusEnum status) {
                Job job = getJob(jobId);
                job.setStatus(status);
                job.setUpdatedAt(Instant.now());
                repository.save(job);

                // STOMP notification removed.
                // For final completion, the Controller's /completed endpoint triggers the
                // WebSocket push.
                // For intermediate updates (RUNNING etc), we might want to push too, but
                // current requirement implies only final result is critical.
                // If needed, we can inject CoreWebSocketHandler here too, but for now removing
                // the broken STOMP code is the priority.
        }
}
