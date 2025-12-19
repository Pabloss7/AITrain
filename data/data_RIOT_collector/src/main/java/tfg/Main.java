package tfg;


import io.github.cdimascio.dotenv.Dotenv;
import com.google.gson.JsonObject;
import com.google.gson.JsonParser;

public class Main {
    public static void main(String[] args) {


        try {
            Dotenv dotenv = Dotenv.load();
            String apikey = dotenv.get("RIOT_API_KEY");
            String accountURI = dotenv.get("RIOT_ACCOUNT_URL");
            String matchesURI = dotenv.get("RIOT_MATCHES_URL");
            String MONGO_URI = dotenv.get("MONGO_URI");
            String MONGO_DB = dotenv.get("MONGO_DB");


            Database db = new Database(
                    MONGO_URI,
                    MONGO_DB
            );
            RiotApiClient client = new RiotApiClient(apikey, db);
            String summonerName = "xxkattaa";
            String tagLine = "KOI";

            String summonerJSON = client.getAccount(
                    accountURI + summonerName + "/" + tagLine
            );

            JsonObject obj = JsonParser.parseString(summonerJSON).getAsJsonObject();
            String puuid = obj.get("puuid").getAsString();


            client.startCollectionOfData(puuid,matchesURI);


        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}