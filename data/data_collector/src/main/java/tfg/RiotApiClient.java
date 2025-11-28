package tfg;

import com.google.gson.Gson;
import com.google.gson.JsonArray;
import com.google.gson.JsonObject;
import com.google.gson.JsonParser;
import io.github.cdimascio.dotenv.Dotenv;
import org.bson.Document;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.*;

public class RiotApiClient {

    private final String apiKey;
    private final Database db;
    private boolean firstIteration = true;
    private String [] PUUIDS;

    public RiotApiClient(String apiKey,  Database db) {
        this.apiKey = apiKey;
        this.db = db;
    }

    public String getAccount(String url_riot) throws Exception {
        URL url = new URL(url_riot);
        HttpURLConnection connection = (HttpURLConnection) url.openConnection();

        connection.setRequestMethod("GET");
        connection.setRequestProperty("X-Riot-Token", this.apiKey);

        BufferedReader br = new BufferedReader(new InputStreamReader(connection.getInputStream()));
        String inputLine;
        StringBuilder content = new StringBuilder();
        while ((inputLine = br.readLine()) != null) {
            content.append(inputLine);
        }

        br.close();
        connection.disconnect();

        return content.toString();
    }

    public void startCollectionOfData(String playerPUUID, String Url) throws Exception {
        int maxMatches = 5000;
        int totalMatches = 0;
        Queue<String> playersQueue = new LinkedList<>();
        Set<String> playersSet = new HashSet<>();

        playersQueue.add(playerPUUID);

        Dotenv dotenv = Dotenv.load();
        String matchesURI = dotenv.get("RIOT_MATCHES_URL");

        while (!playersQueue.isEmpty() && totalMatches < maxMatches) {
            String currentPlayerPUUID = playersQueue.poll();
            System.out.println("Fetching player:"+currentPlayerPUUID);

            if(playersSet.contains(currentPlayerPUUID)) continue;

            // OBTAIN THE MATCHES IDS FROM THE ENTRY PLAYER ACCOUNT
            String completeUrl = Url+"by-puuid/"+currentPlayerPUUID+"/ids?type=ranked&start=0&count=10";
            URL url = new URL(completeUrl);
            HttpURLConnection connection = (HttpURLConnection) url.openConnection();
            connection.setRequestMethod("GET");
            connection.setRequestProperty("X-Riot-Token", this.apiKey);

            BufferedReader br = new BufferedReader(new InputStreamReader(connection.getInputStream()));
            String inputLine;

            StringBuilder content = new StringBuilder();
            while ((inputLine = br.readLine()) != null) {
                content.append(inputLine);
            }
            br.close();
            connection.disconnect();

            Gson gson = new Gson();
            String [] matchIds = gson.fromJson(content.toString(), String[].class);
            System.out.println("Fetched "+matchIds.length+" matches");

            for(String matchId : matchIds){
                if(totalMatches >= maxMatches) break;

                Document doc = getMatch(matchId,matchesURI);

                db.insertResponse(doc);
                System.out.println("Inserted match");
                totalMatches++;

                // Forcing delay so we have rate limits of 100 calls every 2 min,
                // so won't be banned from riot
                Thread.sleep(1200);

                String [] participantsPUUIDS = getPuuids(doc);

                for( String PUUID : participantsPUUIDS){
                   if(!playersSet.contains(PUUID)) playersQueue.add(PUUID);
                   System.out.println("Inserted player:"+PUUID);
                }
            }
            playersSet.add(currentPlayerPUUID);
        }
    }

    public String [] getPuuids(Document content) throws Exception {
        Document metadata = (Document) content.get("metadata");
        List<String> participants = (List<String>) metadata.get("participants");
        return participants.toArray(new String[0]);
    }

    public Document getMatch(String matchId, String Url) throws Exception {
        String completeUrl = Url+matchId;
        URL url = new URL(completeUrl);

        HttpURLConnection connection = (HttpURLConnection) url.openConnection();
        connection.setRequestMethod("GET");
        connection.setRequestProperty("X-Riot-Token", this.apiKey);

        BufferedReader br = new BufferedReader(new InputStreamReader(connection.getInputStream()));
        String inputLine;

        StringBuilder content = new StringBuilder();
        while ((inputLine = br.readLine()) != null) {
            content.append(inputLine);
        }
        br.close();
        connection.disconnect();
        System.out.println("Match with id:"+matchId+" found");
        return Document.parse(content.toString());
    }
}