from django.db import models

class Ruolo( models.Model ):
    tipologia_ruolo = models.CharField( max_length=100 )
    def __str__(self):
        return self.tipologia

class Users(models.Model):
    username = models.CharField(max_length=10)
    password = models.CharField(max_length=100)
    ruolo = models.ForeignKey(Ruolo, on_delete=models.DO_NOTHING,null=True)

class Sesso(models.Model):
    tipologia_sesso = models.CharField(max_length=1)
    def __str__(self):
        return self.tipologia_sesso

class FasciaPrezzo(models.Model):
    fascia_min = models.IntegerField(null=True)
    fascia_max = models.IntegerField(null=True)
    def __str__(self):
        return str(self.fascia_min) + " - " + str(self.fascia_max)

class Contratto(models.Model):
    tipologia_contratto = models.CharField(max_length=50)
    def __str__(self):
        return self.tipologia_contratto

class TipologiaImmobile(models.Model):
    nome_tipologia = models.CharField(max_length=500)

class Cliente(models.Model):
    nome = models.CharField(max_length=100)
    cognome = models.CharField(max_length=100)
    email = models.EmailField(null=True)
    citta = models.CharField(max_length=200)
    telefono_fisso = models.CharField(max_length=10)
    telefono_cellulare = models.CharField(max_length=10)
    cliente = models.CharField(max_length=100)
    scadenza = models.DateField(null=True)
    inizio_incarico = models.DateField(null=True)
    fine_incarico = models.DateField(null=True)

    def __str__(self):
        return str(self.nome) + " " + str(self.cognome)

class Immobile(models.Model):
    data = models.DateField(auto_now_add = True, null=True)
    indirizzo = models.CharField(max_length=100)
    stato = models.CharField(max_length=100)
    citta = models.CharField(max_length=100)
    zona = models.CharField(max_length=5000)
    mutuo = models.CharField(max_length=2)
    immobili_proposti = models.CharField(max_length=5000)
    prezzo = models.IntegerField()
    tipologia = models.CharField(max_length=200, null=True)
    contratto = models.ForeignKey(Contratto, on_delete=models.DO_NOTHING, null=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.DO_NOTHING, null=True)
    note = models.CharField(max_length=5000, null=True)
    fascia_prezzo = models.ForeignKey(FasciaPrezzo, on_delete=models.DO_NOTHING, null=True)

    def __str__(self):
        return self.indirizzo
    # def __str__(self):
    #     return {
    #             self.data,
    #             self.indirizzo,
    #             self.stato,
    #             self.citta,
    #             self.zona,
    #             self.mutuo,
    #             self.immobili_proposti,
    #             self.prezzo,
    #             self.tipologia,
    #             str(self.cliente.nome) + " " + (self.cliente.cognome),
    #             self.note,
    #             str(self.fascia_prezzo.fascia_max) + " - " + str(self.fascia_prezzo.fascia_max)
    #             }
