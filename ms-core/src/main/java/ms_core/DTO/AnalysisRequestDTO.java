package ms_core.DTO;

import jakarta.validation.constraints.NotBlank;
import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class AnalysisRequestDTO {

    @NotBlank
    private String summonerName;

    @NotBlank
    private String TagLine;
}
