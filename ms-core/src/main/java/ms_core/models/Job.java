package ms_core.models;

import jakarta.persistence.*;
import lombok.*;
import ms_core.models.JobStatus.JobStatusEnum;

import java.time.Instant;
import java.util.UUID;

@Entity
@Table(name = "jobs")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class Job {
    @Id
    @Column(nullable = false,updatable = false)
    private UUID jobId;

    @Column(nullable = false)
    private String summonerName;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    private JobStatusEnum status;

    @Column(nullable = false)
    private Instant createdAt;

    private Instant updatedAt;
}
