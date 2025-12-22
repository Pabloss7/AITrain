package ms_core.service;

import lombok.RequiredArgsConstructor;
import ms_core.DTO.DataAnalysisRequest;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

@Service
@RequiredArgsConstructor
public class DataService {
   private final RestTemplate restTemplate;

   @Value("${services.data.url}")
    private String url;
   //TODO: keep developing ms-core to data-ms connection
   public  void starAnalysis(DataAnalysisRequest request){
       restTemplate.postForEntity(
               url+"/analysis",
               request,
               Void.class
       );
   }
}
