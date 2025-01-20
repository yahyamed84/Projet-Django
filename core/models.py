from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

class Wilaya(models.Model):
    nom = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=10, unique=True)
    
    def __str__(self):
        return self.nom
    
    class Meta:
        verbose_name = 'Wilaya'
        verbose_name_plural = 'Wilayas'

class Moughataa(models.Model):
    nom = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    wilaya = models.ForeignKey(Wilaya, on_delete=models.CASCADE, related_name='moughataas')
    
    def __str__(self):
        return f"{self.nom} ({self.wilaya.nom})"
    
    class Meta:
        verbose_name = 'Moughataa'
        verbose_name_plural = 'Moughataas'

class Commune(models.Model):
    nom = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    moughataa = models.ForeignKey(Moughataa, on_delete=models.CASCADE, related_name='communes')
    
    def __str__(self):
        return f"{self.nom} ({self.moughataa.nom})"
    
    class Meta:
        verbose_name = 'Commune'
        verbose_name_plural = 'Communes'

class FamilleProduit(models.Model):
    nom = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.nom} ({self.code})"
    
    class Meta:
        verbose_name = 'Famille de produits'
        verbose_name_plural = 'Familles de produits'
        ordering = ['nom']

class Produit(models.Model):
    code = models.CharField(max_length=20, unique=True)
    nom = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    unite_mesure = models.CharField(max_length=50)
    famille = models.ForeignKey(FamilleProduit, on_delete=models.PROTECT, related_name='produits')
    date_creation = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.nom} ({self.code})"
    
    class Meta:
        verbose_name = 'Produit'
        verbose_name_plural = 'Produits'
        ordering = ['famille', 'nom']

class PanierProduits(models.Model):
    nom = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.nom
    
    class Meta:
        verbose_name = 'Panier de produits'
        verbose_name_plural = 'Paniers de produits'

class ProduitPanier(models.Model):
    panier = models.ForeignKey(PanierProduits, on_delete=models.CASCADE, related_name='produits')
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    ponderation = models.DecimalField(max_digits=5, decimal_places=2, default=1.00)
    date_debut = models.DateField()
    date_fin = models.DateField()

    class Meta:
        verbose_name = "Produit dans le panier"
        verbose_name_plural = "Produits dans le panier"
        unique_together = ('panier', 'produit')

    def __str__(self):
        return f"{self.produit.nom} dans {self.panier.nom}"

class PointVente(models.Model):
    nom = models.CharField(max_length=200)
    commune = models.ForeignKey(Commune, on_delete=models.CASCADE, related_name='points_vente')
    latitude = models.DecimalField(max_digits=10, decimal_places=6)
    longitude = models.DecimalField(max_digits=10, decimal_places=6)
    adresse = models.TextField()
    date_creation = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.nom} ({self.commune.nom})"
    
    class Meta:
        verbose_name = 'Point de vente'
        verbose_name_plural = 'Points de vente'

class PrixProduit(models.Model):
    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('validé', 'Validé'),
        ('rejeté', 'Rejeté'),
    ]

    produit = models.ForeignKey(Produit, on_delete=models.CASCADE, related_name='prix')
    point_vente = models.ForeignKey(PointVente, on_delete=models.CASCADE, related_name='prix')
    prix = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    date_releve = models.DateTimeField(default=timezone.now)
    date_saisie = models.DateTimeField(auto_now_add=True)
    statut = models.CharField(
        max_length=20,
        choices=STATUT_CHOICES,
        default='en_attente'
    )
    
    class Meta:
        verbose_name = 'Prix de produit'
        verbose_name_plural = 'Prix des produits'
        unique_together = ['produit', 'point_vente', 'date_releve']
        indexes = [
            models.Index(fields=['date_releve']),
            models.Index(fields=['produit', 'date_releve']),
        ]
