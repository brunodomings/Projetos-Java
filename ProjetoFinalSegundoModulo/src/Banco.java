import java.util.Scanner;

public class Banco {
    public static void main(String[] args) {
        String nome = "Yasmin Novaes";
        String tipoConta = "Corrente";
        double saldo = 1000.00;
        
        System.out.println("***************************");
        System.out.println("\nBem-vindo ao Banco XYZ!");
        System.out.println("Nome do cliente: " + nome);
        System.out.println("Tipo de conta: " + tipoConta);
        System.out.println("Saldo atual: R$ " + saldo);
        System.out.println("\n***************************");

        int opcao = 0;

        String menu = """
            ***Digite a opção desejada:***
            1 - Consultar saldo
            2 - Transferir
            3 - Receber valor
            4 - Sair
            """;
    
        Scanner Leitura = new Scanner(System.in);
            
        while (opcao != 4) {
            System.out.println(menu);
            opcao = Leitura.nextInt();

            if (opcao == 1) {
                System.out.println("Saldo atual da conta: R$ " + saldo);

            } else if (opcao == 2) {
                System.out.println("Qual quantia deseja transferir?");
                double valor = Leitura.nextDouble();
                if (valor > saldo){
                    System.out.println("Saldo insuficiente para realizar a transferência.");
                } else {
                    saldo -= valor;
                    System.out.println("Novo saldo R$: " + saldo);
                }

            } else if (opcao == 3) {
                System.out.println("Valor");
                double valor = Leitura.nextDouble();
                saldo += valor;
                System.out.println("Novo saldo R$: " + saldo);

            } else if (opcao == 4) {
                System.out.println("Saindo do sistema. Até logo!");

            } else {
                System.out.println("Opção inválida! Escolha entre 1 e 4.");
            }   
        }
        
        Leitura.close();
    }
}