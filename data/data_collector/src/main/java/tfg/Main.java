package tfg;


import io.github.cdimascio.dotenv.Dotenv;

public class Main {
    public static void main(String[] args) {


        try {
            // TODO: mover responsabilidades a otra clase + introducir el bucle para 10k games
            Dotenv dotenv = Dotenv.load();
            String apikey = dotenv.get("RIOT_API_KEY");
            String accountURI = dotenv.get("RIOT_ACCOUNT_URL");
            String matchesURI = dotenv.get("RIOT_MATCHES_URL");


            RiotApiClient client = new RiotApiClient(apikey);
            Database db = new Database("jdbc:sqlite:db");

            String summonerName = "xxkattaa";
            String tagLine = "KOI";

            String summonerJSON = client.get(
                    accountURI + summonerName + "/" + tagLine
            );

            System.out.println(summonerJSON);

        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}