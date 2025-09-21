import java.util.Scanner;
import java.util.Random;

// Clase base
class Juego {
    protected int numeroDeVidas;
    protected int record;

    public Juego(int numeroDeVidas) {
        this.numeroDeVidas = numeroDeVidas;
        this.record = 0;
    }

    public void reiniciaPartida() {
        System.out.println("Partida reiniciada.Tienes " + numeroDeVidas + " vidas");
    }

    public void actualizaRecord() {
        if (numeroDeVidas > record) {
            record = numeroDeVidas;
            System.out.println("Nuevo récord Vidas sobrantes: " + record);
        }
    }

    public boolean quitaVida() {
        numeroDeVidas--;
        if (numeroDeVidas > 0) {
            System.out.println("Te queda " + numeroDeVidas + " vida(s).");
            return true;
        } else {
            System.out.println("Perdiste todas tus vidas :( )");
            return false;
        }
    }
}

// Clase derivada
class JuegoAdivinaNumero extends Juego {
    private int numeroAAdivinar;

    public JuegoAdivinaNumero(int vidas) {
        super(vidas);
    }

    public void juega() {
        reiniciaPartida();

        Random random = new Random();
        numeroAAdivinar = random.nextInt(11); 

        Scanner sc = new Scanner(System.in);

        while (true) {
            System.out.print("Adivina un número entre 0 y 10: ");
            int intento = sc.nextInt();

            if (intento == numeroAAdivinar) {
                System.out.println("lo hiciste bien");
                actualizaRecord();
                break;
            } else {
                if (quitaVida()) {
                    if (intento < numeroAAdivinar) {
                        System.out.println("El número a adivinar es mayor.");
                    } else {
                        System.out.println("El número a adivinar es menor.");
                    }
                } else {
                    break; // se quedó sin vidas
                }
            }
        }
    }
}

// Clase principal con main
public class Ejercicio1 {
    public static void main(String[] args) {
        JuegoAdivinaNumero j1 = new JuegoAdivinaNumero(3); // 3 vidas
        j1.juega();
    }
}
