package data_collector.DTO;

import lombok.Builder;
import lombok.Data;
import lombok.Getter;
import lombok.Setter;
import lombok.experimental.SuperBuilder;

import java.util.Map;

@Setter
@Getter
@Builder
public class MatchAISenderDTO {
    String jobId;
    String matchId;
    String puuid;
    Map<String, Object> metadata;
    Map<String, Object> info;
}
