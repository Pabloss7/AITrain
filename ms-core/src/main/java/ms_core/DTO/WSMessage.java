package ms_core.DTO;

import lombok.Data;

@Data
public class WSMessage {
    private String type;
    private Object payload;

    public static WSMessage of(String type, Object payload) {
        WSMessage msg = new WSMessage();
        msg.type = type;
        msg.payload = payload;
        return msg;
    }
}

