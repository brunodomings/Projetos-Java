package calculo;

public class Recomendacao {
    private String recomandacao;

    public void filra(Classificavel classificavel) {
        if (classificavel.getClassificacao() >= 4) {
            System.out.println("Esta entre os preferidos do momento");
        } else if (classificavel.getClassificacao() >= 2) {
            System.out.println("Muito bem avalidado no momento!");
        } else {
            System.out.println("Cloloque na sua Lista para assistir depois");
        }
    }
}
