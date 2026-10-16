package models;

public class Musica extends Audio{
    private String album;
    private String cantor;
    private String gerero;

    public String getAlbum() {
        return album;
    }

    public void setAlbum(String album) {
        this.album = album;
    }

    public String getCantor() {
        return cantor;
    }

    public void setCantor(String cantor) {
        this.cantor = cantor;
    }

    public String getGerero() {
        return gerero;
    }

    public void setGerero(String gerero) {
        this.gerero = gerero;
    }

    @Override 
    public int getClassificacao() {
        if (this.getTotalReproducoes() > 2000) {
            return 10;
        } else {
            return 8;
        }
    }
}
