package data_collector.service;

import com.google.gson.JsonArray;
import com.google.gson.JsonObject;
import com.google.gson.JsonParser;
import io.github.cdimascio.dotenv.Dotenv;
import org.springframework.http.HttpStatus;
import org.springframework.web.reactive.function.client.WebClient;


public class RiotAPIService {
    Dotenv dotenv = Dotenv.load();
    String apiKey = dotenv.get("RIOT_API_KEY");
    String accountURI = dotenv.get("RIOT_ACCOUNT_URL");
    String matchesURI = dotenv.get("RIOT_MATCHES_URL");
    private final WebClient webClient = WebClient.builder().build();

    public String getSingleMatch(String summonerName, String tagLine){
       try{
           String summonerJSON = getAccount(summonerName,tagLine);
           JsonObject obj = JsonParser.parseString(summonerJSON).getAsJsonObject();
           String playerPUUID = obj.get("puuid").getAsString();

          return getMatch(playerPUUID);
       }catch(Exception e){
           return null;
       }
    }

    private String getMatch(String playerPUUID){
       try{
           String url = matchesURI+"by-puuid/"+playerPUUID+"/ids?type=ranked&start=0&count=1";

           String ids = webClient.get()
                   .uri(url)
                   .header("X-Riot-Token", apiKey)
                   .retrieve()
                   .bodyToMono(String.class)
                   .block();
           JsonArray idsArray = JsonParser.parseString(ids).getAsJsonArray();
           String matchID = idsArray.get(0).getAsString();
           String matchInfoUrl = matchesURI+matchID;

           String match  = webClient.get()
                   .uri(matchInfoUrl)
                   .header("X-Riot-Token", apiKey)
                   .retrieve()
                   .bodyToMono(String.class)
                   .block();
           JsonObject matchJSON = JsonParser.parseString(match).getAsJsonObject();

        //  webClient.post()
        //          .uri(//LA URL DEL MS DE PYHON)
        //          .body(matchJSON)
            System.out.println(matchJSON);
            return  matchJSON.toString();
       }catch(Exception e){
            return HttpStatus.INTERNAL_SERVER_ERROR.toString();
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
}
