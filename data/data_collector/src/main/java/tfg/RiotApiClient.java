package tfg;

import com.google.gson.Gson;
import com.google.gson.JsonArray;
import com.google.gson.JsonObject;
import com.google.gson.JsonParser;
import io.github.cdimascio.dotenv.Dotenv;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;

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
        // OBTAIN THE MATCHES IDS FROM THE ENTRY PLAYER ACCOUNT
        String completeUrl = Url+"by-puuid/"+playerPUUID+"/ids?type=ranked&start=0&count=2";
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

        Dotenv dotenv = Dotenv.load();
        String matchesURI = dotenv.get("RIOT_MATCHES_URL");

        for(String matchId : matchIds){
            getMatch(matchId,matchesURI);
        }

        for (String puuid : PUUIDS) {
            System.out.println(puuid);
        }
    }

    public String [] getPuuids(StringBuilder content) throws Exception {

        JsonObject obj = JsonParser.parseString(content.toString()).getAsJsonObject();
        JsonArray puuids = obj.getAsJsonObject("metadata").getAsJsonArray("participants");

        String [] puuidIds = new String[puuids.size()];
        for (int i = 0; i < puuids.size(); i++) {
            puuidIds[i] = puuids.get(i).getAsString();
        }

        return puuidIds;
    }

    public void getMatch(String matchId, String Url) throws Exception {
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

        if(firstIteration){
            PUUIDS = getPuuids(content);
            firstIteration = false;
        }
        db.insertResponse(content.toString());
    }
}