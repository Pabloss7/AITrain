package tfg;

import com.google.gson.JsonObject;
import com.mongodb.client.MongoClient;
import com.mongodb.client.MongoClients;
import com.mongodb.client.MongoCollection;
import com.mongodb.client.MongoDatabase;
import org.bson.Document;

import java.sql.*;

public class Database {

    private final MongoClient client;
    private  final MongoDatabase database;
    private  final MongoCollection<Document> responses;

    public Database(String uri, String dbName) throws  Exception {
        client = MongoClients.create(uri);
        database = client.getDatabase(dbName);
        responses = database.getCollection("responses");
    }

    public void insertResponse(Document json) throws SQLException {
       Document doc = new Document("json", json);
       responses.insertOne(doc);
    }

}