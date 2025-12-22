package ms_core.DTO;

import lombok.AllArgsConstructor;
import lombok.Getter;
import ms_core.models.JobStatus.JobStatusEnum;
import java.util.UUID;

@Getter
@AllArgsConstructor
public class JobStatusResponseDTO {
    private UUID id;
    private JobStatusEnum status;
}
