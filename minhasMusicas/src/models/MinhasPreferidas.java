package models;

public class MinhasPreferidas {
    public void inclui(Audio audio) {
        if (audio.getClassificacao() >= 9) {
            System.out.println(audio.getTitulo() + " é conciderado sucesso absoluto");
        } else {
            System.out.println(audio.getTitulo() + " é um sucesso");
        }
    }
}
