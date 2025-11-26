package tfg;

import java.sql.*;

public class Database {

    private final Connection connection;

    public Database(String uri) throws  Exception {
        connection = DriverManager.getConnection(uri);
        createTable();
    }

    private void createTable() throws SQLException {
        String sql = "CREATE TABLE IF NOT EXISTS responses (id INTEGER PRIMARY KEY AUTOINCREMENT, json TEXT)";
        Statement stmt = connection.createStatement();
        stmt.execute(sql);
    }

    public void insertResponse(String json) throws SQLException {
        String sql = "INSERT INTO responses (json) VALUES (?)";
        PreparedStatement stmt = connection.prepareStatement(sql);
        stmt.setString(1, json);
        stmt.executeUpdate();
    }

}