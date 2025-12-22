package data_collector.service;

import com.google.gson.Gson;
import com.google.gson.JsonArray;
import com.google.gson.JsonObject;
import com.google.gson.JsonParser;
import data_collector.DTO.MatchAISenderDTO;
import io.github.cdimascio.dotenv.Dotenv;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Service;
import org.springframework.web.reactive.function.client.WebClient;
import org.springframework.web.server.ResponseStatusException;
import tools.jackson.databind.ObjectMapper;

import java.util.Map;

@Service
public class RiotAPIService {
    Dotenv dotenv = Dotenv.configure()
            .ignoreIfMissing()
            .load();
        
    String apiKey = dotenv.get("RIOT_API_KEY");
    String accountURI = dotenv.get("RIOT_ACCOUNT_URL");
    String matchesURI = dotenv.get("RIOT_MATCHES_URL");
    private final WebClient webClient = WebClient.builder().build();

    public MatchAISenderDTO getSingleMatch(String summonerName, String tagLine, String jobId){
           String summonerJSON = getAccount(summonerName,tagLine);
           JsonObject obj = JsonParser.parseString(summonerJSON).getAsJsonObject();
           String playerPUUID = obj.get("puuid").getAsString();

          return getMatch(playerPUUID, jobId);
    }

    private MatchAISenderDTO getMatch(String playerPUUID, String jobId){
       try{
            String url = matchesURI+"by-puuid/"+playerPUUID+"/ids?type=ranked&start=0&count=1";

            String ids = webClient.get()
                    .uri(url)
                    .header("X-Riot-Token", apiKey)
                    .retrieve()
                    .bodyToMono(String.class)
                    .block();
            JsonArray idsArray = JsonParser.parseString(ids).getAsJsonArray();
            if(idsArray.isEmpty()){
                throw new ResponseStatusException(HttpStatus.NOT_FOUND, "No games found");
            }
            String matchID = idsArray.get(0).getAsString();
            String matchInfoUrl = matchesURI+matchID;

            String match  = webClient.get()
                    .uri(matchInfoUrl)
                    .header("X-Riot-Token", apiKey)
                    .retrieve()
                    .bodyToMono(String.class)
                    .block();
            JsonObject matchJSON = JsonParser.parseString(match).getAsJsonObject();

            MatchAISenderDTO matchDTO = buildMatchDTO(jobId,playerPUUID,matchJSON, matchID);

            String ai_url = dotenv.get("AI_URL");
            String URL = ai_url+"/analyze-match";

            webClient.post()
                    .uri(URL)
                    .header(HttpHeaders.CONTENT_TYPE, "application/json")
                    .bodyValue(matchDTO)
                    .retrieve()
                    .bodyToMono(Void.class)
                    .doOnSuccess(v -> System.out.println("Request sent to AI microservice"))
                    .doOnError(e -> System.out.println("Error calling AI microservice: \n"+e))
                    .subscribe();

            webClient.patch()
                    .uri("http://ms-core:8181/analysis/"+jobId+"/running")
                    .subscribe();

            ObjectMapper mapper = new ObjectMapper();
            System.out.println(
            "Sending to AI ms: \n" + mapper.writerWithDefaultPrettyPrinter().writeValueAsString(matchDTO)
            );
            return  matchDTO;
       }catch(Exception e){
         if(e instanceof ResponseStatusException){
             throw e;
         }else{
             throw new ResponseStatusException(HttpStatus.INTERNAL_SERVER_ERROR, e.getMessage());
         }
       }
    }

    private String getAccount(String summonerName, String tagLine){
        try{
            String url = accountURI+summonerName+ "/"+ tagLine;
            return webClient.get()
                    .uri(url)
                    .header("X-Riot-Token", apiKey)
                    .retrieve()
                    .bodyToMono(String.class)
                    .block();

        }catch(Exception e){
            return HttpStatus.INTERNAL_SERVER_ERROR.toString();
        }
    }
    private MatchAISenderDTO buildMatchDTO(String jobId, String puuid, JsonObject matchJSON, String matchId){
        Gson gson = new Gson();
        Map<String, Object> metada = gson.fromJson(matchJSON.getAsJsonObject("metadata"), Map.class);
        Map<String, Object> info = gson.fromJson(matchJSON.getAsJsonObject("info"), Map.class);

        return  MatchAISenderDTO.builder()
                .jobId(jobId)
                .puuid(puuid)
                .matchId(matchId)
                .metadata(metada)
                .info(info)
                .build();
    }
}
