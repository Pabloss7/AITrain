package tfg;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;

public class RiotApiClient {

    private final String apiKey;

    public RiotApiClient(String apiKey) {
        this.apiKey = apiKey;
    }

    public String get(String url_riot) throws Exception {
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
}