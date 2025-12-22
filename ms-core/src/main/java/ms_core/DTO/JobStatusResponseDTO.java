package ms_core.DTO;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.Setter;
import ms_core.models.JobStatus.JobStatusEnum;
import java.util.UUID;

@Getter
@Setter
@Builder
@AllArgsConstructor
public class JobStatusResponseDTO {
    private UUID id;
    private JobStatusEnum status;
}
