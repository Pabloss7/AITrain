package data_collector.DTO;

import lombok.Getter;
import lombok.Setter;

@Setter
@Getter
public class AnalyzeMatchRequestDTO {
    private String jobId;
    private String summonerName;
    private String tagLine;
}
