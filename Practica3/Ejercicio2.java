import java.util.Random;
import java.util.Scanner;

// Clase padre
class Juego {
    protected int numeroDeVidas;
    protected int record;

    public Juego(int numeroDeVidas) {
        this.numeroDeVidas = numeroDeVidas;
        this.record = 0;
    }

    public void reiniciaPartida() {
        System.out.println("Partida reiniciada. Nro de Vidas: " + numeroDeVidas);
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
            System.out.println("Te queda " + numeroDeVidas + " vidas.");
            return true;
        } else {
            System.out.println("Perdiste todas las vidas");
            return false;
        }
    }
}

// Clase derivada
class JuegoAdivinaNumero extends Juego {
    protected int numeroAAdivinar;

    public JuegoAdivinaNumero(int vidas) {
        super(vidas);
    }

    public boolean validaNumero(int num) {
        return num >= 0 && num <= 10;
    }

    public void juega() {
        reiniciaPartida();

        Random random = new Random();
        numeroAAdivinar = random.nextInt(11);

        Scanner sc = new Scanner(System.in);

        while (true) {
            System.out.print("Adivina un número entre 0 y 10: ");
            int intento = sc.nextInt();

            if (!validaNumero(intento)) {
                System.out.println("Número inválido, intente de nuevo.");
                continue;
            }

            if (intento == numeroAAdivinar) {
                System.out.println("Acertaste el numero!");
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
                    break;
                }
            }
        }
    }
}

// Juego de números pares
class JuegoAdivinaPar extends JuegoAdivinaNumero {
    public JuegoAdivinaPar(int vidas) {
        super(vidas);
    }

    @Override
    public boolean validaNumero(int num) {
        if (num < 0 || num > 10) return false;
        if (num % 2 != 0) {
            System.out.println("Error: el número no es par.");
            return false;
        }
        return true;
    }
}

// Juego de números impares
class JuegoAdivinaImpar extends JuegoAdivinaNumero {
    public JuegoAdivinaImpar(int vidas) {
        super(vidas);
    }

    @Override
    public boolean validaNumero(int num) {
        if (num < 0 || num > 10) return false;
        if (num % 2 == 0) {
            System.out.println("Error: el número no es impar.");
            return false;
        }
        return true;
    }
}

// Clase principal
public class Ejercicio2 {
    public static void main(String[] args) {
        System.out.println("----------- Juego Adivina Número -----------");
        JuegoAdivinaNumero j1 = new JuegoAdivinaNumero(3);
        j1.juega();

        System.out.println("\n----------- Juego Adivina Número Par -----------");
        JuegoAdivinaPar j2 = new JuegoAdivinaPar(3);
        j2.juega();

        System.out.println("\n----------- Juego Adivina Número Impar -----------");
        JuegoAdivinaImpar j3 = new JuegoAdivinaImpar(3);
        j3.juega();
    }
}
