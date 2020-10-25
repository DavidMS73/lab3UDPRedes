package sevidor;
import java.net.ServerSocket;
import java.net.Socket;

public class Servidor {
    private static final String RUTA = "data/";
    public Servidor() {
        String[] grupos = {"225.1.2.3", "225.2.3.4", "225.3.4.5"};
        try {
            for(int i=0;i<3;i++) { // inicializacion de un nuevo canal en el socket
                new Thread(new Canal(RUTA+(i+1)+".mp4",i+1,grupos[i])).start();
            }

        } catch (Exception e) {
            System.out.println("-------------------------------");
            System.out.println("ERROR SERVIDOR: ");
            System.out.println(e.getMessage());
            System.out.println(e.getCause());
            System.out.println("-------------------------------");
        }
    }

    public static void main(String[] args) {
        new Servidor();
    }
}