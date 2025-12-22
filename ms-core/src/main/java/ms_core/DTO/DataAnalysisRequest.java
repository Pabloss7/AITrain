package ms_core.DTO;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.Setter;

import java.util.UUID;

@Getter
@Setter
@Builder
@AllArgsConstructor
public class DataAnalysisRequest {
    private UUID id;
    private String summonerName;
    private String tagLine;
}
