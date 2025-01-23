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
    produits = models.ManyToManyField(Produit, through='ProduitPanier', related_name='paniers')
    
    def __str__(self):
        return self.nom
    
    class Meta:
        verbose_name = 'Panier de produits'
        verbose_name_plural = 'Paniers de produits'

class ProduitPanier(models.Model):
    panier = models.ForeignKey(PanierProduits, on_delete=models.CASCADE, null=True, blank=True)
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    ponderation = models.DecimalField(max_digits=5, decimal_places=2, default=1.0)
    date_debut = models.DateField(auto_now_add=True)
    date_fin = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name = "Produit du panier"
        verbose_name_plural = "Produits du panier"
        indexes = [
            models.Index(fields=['produit', 'date_debut']),
        ]
        
    def __str__(self):
        return f"{self.produit.nom} - Pondération: {self.ponderation}"

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

class INPC(models.Model):
    mois = models.DateField(verbose_name="Mois de calcul")
    valeur = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valeur de l'INPC")
    date_calcul = models.DateTimeField(auto_now_add=True, verbose_name="Date de calcul")
    
    class Meta:
        verbose_name = "INPC"
        verbose_name_plural = "INPC"
        ordering = ['-mois']
        
    def __str__(self):
        return f"INPC {self.mois.strftime('%B %Y')} : {self.valeur}"
        
    @classmethod
    def calculer_inpc(cls, mois):
        """
        Calcule l'INPC pour un mois donné.
        Le mois doit être un objet date du premier jour du mois.
        """
        from django.db import connection
        import logging
        logger = logging.getLogger(__name__)
        
        # Vérifier si l'INPC existe déjà pour ce mois
        inpc_existant = cls.objects.filter(mois=mois).first()
        if inpc_existant:
            return inpc_existant
        
        # Récupérer tous les prix validés du mois
        debut_mois = mois
        fin_mois = (mois.replace(day=28) + timezone.timedelta(days=4)).replace(day=1) - timezone.timedelta(days=1)
        
        logger.info(f"Calcul INPC pour la période du {debut_mois} au {fin_mois}")
        
        # Récupérer le panier de référence (le plus récent)
        panier = PanierProduits.objects.order_by('-date_creation').first()
        if not panier:
            raise ValueError("Aucun panier de référence n'a été défini")
            
        logger.info(f"Utilisation du panier : {panier.nom}")
        
        # Calculer la moyenne pondérée des variations de prix
        somme_ponderee = 0
        poids_total = 0
        produits_sans_prix = []
        
        produits_panier = ProduitPanier.objects.filter(
            panier=panier,
            date_fin__isnull=True
        ).select_related('produit')
        
        logger.info(f"Nombre de produits dans le panier : {produits_panier.count()}")
        
        # D'abord, trouvons les derniers prix validés pour chaque produit
        for produit_panier in produits_panier:
            # Chercher le dernier prix validé pour ce produit
            dernier_prix = PrixProduit.objects.filter(
                produit=produit_panier.produit,
                statut='validé'
            ).order_by('-date_releve').first()
            
            if dernier_prix:
                logger.info(f"Produit {produit_panier.produit.nom}: Utilisation du dernier prix validé = {dernier_prix.prix} du {dernier_prix.date_releve}")
                somme_ponderee += dernier_prix.prix * produit_panier.ponderation
                poids_total += produit_panier.ponderation
            else:
                produits_sans_prix.append(produit_panier.produit.nom)
                logger.warning(f"Aucun prix validé trouvé pour le produit {produit_panier.produit.nom}")
        
        logger.info(f"Somme pondérée totale : {somme_ponderee}")
        logger.info(f"Poids total : {poids_total}")
        
        if poids_total == 0:
            message = "Aucun prix validé n'a été trouvé pour les produits du panier."
            if produits_sans_prix:
                message += f" Produits sans prix : {', '.join(produits_sans_prix)}"
            raise ValueError(message)
        
        # Calculer l'INPC
        valeur_inpc = somme_ponderee / poids_total
        
        logger.info(f"INPC calculé : {valeur_inpc}")
        
        # Créer et sauvegarder l'INPC
        return cls.objects.create(
            mois=mois,
            valeur=valeur_inpc
        )
