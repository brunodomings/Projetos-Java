import calculo.CalculadoraDeTempo;
import calculo.FiltroRecomendacao;
import models.Episodio;
import models.Filme;
import models.Serie;

public class Principal {

    public static void main(String[] args) {
        Filme filmeCatalogo = new Filme();

        filmeCatalogo.setNome("The Matrix");
        filmeCatalogo.setAnoDeLancamento(1999);
        filmeCatalogo.setDuracaoEmMinutos(135);
        filmeCatalogo.setIncluidoNoPlano(true);
        System.out.println("Duração do filme " + filmeCatalogo.getDuracaoEmMinutos());
        
        filmeCatalogo.exibeFichaTecnica();
        filmeCatalogo.avalia(9);
        filmeCatalogo.avalia(8);
        filmeCatalogo.avalia(9);

        System.out.println("Média de avaliações do filme: " + filmeCatalogo.pegaMedia());
        
        Serie lost = new Serie();

        lost.setNome("Lost");
        lost.setAnoDeLancamento(2000);
        lost.exibeFichaTecnica();
        lost.setTemporadas(10);
        lost.setEpisodiosPorTemporadas(10);
        lost.setMinutosPorEpisodio(50);
        System.out.println("Duração da serie " + lost.getDuracaoEmMinutos());

        
        Filme filmeCatalogo2 = new Filme();
        filmeCatalogo2.setNome("Avatar");
        filmeCatalogo2.setAnoDeLancamento(2024);
        filmeCatalogo2.setDuracaoEmMinutos(130);
        
        CalculadoraDeTempo calculadora = new CalculadoraDeTempo();
        calculadora.inclui(filmeCatalogo);
        calculadora.inclui(filmeCatalogo2);
        calculadora.inclui(lost);
        System.out.println(calculadora.getTempoTotal());

        FiltroRecomendacao filtro = new FiltroRecomendacao();
        filtro.filtra(filmeCatalogo);

        Episodio episodio = new Episodio();
        episodio.setNumero(1);
        episodio.setSerie(lost);
        episodio.setTotalVisualizacoes(300);
        filtro.filtra(episodio);

    }

}



//para rodar primeiro faça o passo um para ir para pasta certa, depois para compilar, depois para rodas
//cd "D:\trabalhos\Alura\Java\Quarto projeto"
//javac -d . Principal.java models\*.java calculo\*.java
//java Principal