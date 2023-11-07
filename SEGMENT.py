#!/usr/bin/env python
# coding: utf-8

# # Customer Segmentation using RFM

# # Qu'est-ce que l'analyse RFM ?
# L'analyse RFM est une technique utilisée pour catégoriser les clients en fonction de leur comportement d'achat.

# # Comment cela est calculé ?
# Récence : Il s'agit de la date à laquelle le client a effectué son dernier achat. Elle est calculée en soustrayant la date du dernier achat du client à la date d'analyse.
# 
# Fréquence : Il s'agit du nombre total d'achats effectués par le client. Autrement dit, il indique la fréquence des achats réalisés par le client.
# 
# Monétaire : Il s'agit de la valeur monétaire totale dépensée par le client.

# # Le Problème Commercial
# 
# Une entreprise de commerce électronique souhaite segmenter ses clients et déterminer des stratégies marketing en fonction de ces segments. Par exemple, il est souhaitable d'organiser des campagnes différentes pour fidéliser les clients qui sont très rentables pour l'entreprise, et d'autres campagnes pour les nouveaux clients.

# # Ensemble de Données
# 
# L'ensemble de données Online Retail II comprend les ventes d'un magasin de commerce en ligne basé au Royaume-Uni entre le 1er décembre 2009 et le 9 décembre 2011. Le catalogue de produits de cette entreprise comprend des souvenirs. La grande majorité des clients de l'entreprise sont des clients professionnels.

# # Variables
# 
# InvoiceNo : Numéro de facture. Un numéro unique pour chaque transaction. S'il commence par un "C", cela signifie des opérations annulées.
# 
# StockCode : Code produit. Un numéro unique pour chaque produit.
# 
# Description : Nom du produit.
# 
# Quantity : Il fait référence au nombre de produits figurant sur les factures qui ont été vendus.
# 
# InvoiceDate : Date de la facture.
# 
# UnitPrice : Prix du produit (en livres sterling).
# 
# CustomerID : Numéro unique du client.
# 
# Country : Le nom du pays où le client réside.

# In[1]:


#Import 
import datetime as dt
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings # Uyarılar
warnings.filterwarnings("ignore")


# In[3]:


#Lire et copier les donnees
online_retail = pd.read_excel('C:/Users/Fatou Fall/Downloads/archive/online_retail_II.xlsx', sheet_name="Year 2010-2011")
df = online_retail.copy()
df.head()


# In[7]:


def check_df(dataframe):
    print("------------ Shape --------------")
    print(dataframe.shape)
    print("------------  Columns -----------")
    print(dataframe.columns)
    print("------------ Types ------------ ")
    print(dataframe.dtypes)
    print("------------ Head --------------")
    print(dataframe.head())
    print("------------ Tail --------------")
    print(dataframe.tail())
    print("------------  Describe ---------")
    print(dataframe.describe().T)

check_df(df)


# In[21]:


#Y a-t-il des observations manquantes dans l'ensemble de données ?
df.isnull().sum()


# In[9]:


#Supprimer les observations manquantes de l'ensemble de données
df.dropna(inplace=True)


# In[10]:


#Combien d'articles uniques dans l'ensemble de données ?
df["Description"].nunique()


# In[11]:


#Combien de produits dans l'ensemble de données ?
df["Description"].value_counts()


# In[29]:


#Classer les 10 produits les plus commandés du plus au moins commandé 
df.groupby("Description").agg({"Quantity":"sum"}).sort_values("Quantity", ascending=False).head(10)


# In[31]:


top_10_products = df.groupby("Description").agg({"Quantity": "sum"}).sort_values("Quantity", ascending=False).head(10)
plt.figure(figsize=(10, 6))
sns.barplot(x=top_10_products.index, y=top_10_products['Quantity'], palette="coolwarm")
plt.title('Top 10 Produits les Plus Commandés')
plt.xlabel('Description du Produit')
plt.ylabel('Quantité Vendue')
plt.xticks(rotation=90)
plt.show()


# In[13]:


#Supprimer les transactions annulées de l'ensemble de données
df = df[~df["Invoice"].str.contains("C", na=False)]


# In[14]:


#Le montant total de chaque facture et nous créons cette colonne en multipliant 'Prix' et 'Quantité'.
df["TotalPrice"] = df["Quantity"] * df["Price"]


# In[15]:


#Détermination de la date d'analyse pour la recency 
df["InvoiceDate"].max()
today_date = dt.datetime(2011, 12, 11)
rfm = df.groupby('Customer ID').agg({'InvoiceDate': lambda date: (today_date - date.max()).days,
                                     'Invoice': lambda num: num.nunique(),
                                     'TotalPrice': lambda TotalPrice: TotalPrice.sum()})
rfm.columns=["Recency","Frequency","Monetary"]
rfm = rfm[rfm["Monetary"] > 0]
rfm.describe().T


# In[38]:


#Date du dernier achat du client. La date la plus proche obtient 5 et la date la plus éloignée obtient 1..
rfm["recency_score"] = pd.qcut(rfm['Recency'], 5, labels=[5, 4, 3, 2, 1])
# Nombre total d'achats. La fréquence la moins élevée obtient 1 et la fréquence la plus élevée obtient 5.
rfm["frequency_score"] = pd.qcut(rfm["Frequency"].rank(method="first"), 5, labels=[1, 2, 3, 4, 5])
#Dépenses totales par le client. Le moins d'argent obtient 1, le plus d'argent obtient 5.
rfm["monetary_score"]= pd.qcut(rfm["Monetary"],5,labels=[1,2,3,4,5])
rfm.head()

    Recency Score (Score de Récence) : Vous attribuez un score de récence en fonction de la date du dernier achat du client. Le client avec la date d'achat la plus proche obtient un score de 5, tandis que le client avec la date d'achat la plus éloignée obtient un score de 1. Cela catégorise les clients en fonction de la proximité de leur dernier achat, où 5 signifie le plus récent et 1 le moins récent.

    Frequency Score (Score de Fréquence) : Vous attribuez un score de fréquence en fonction du nombre total d'achats effectués par le client. Le client avec la fréquence d'achat la plus faible obtient un score de 1, tandis que le client avec la fréquence d'achat la plus élevée obtient un score de 5. Cela classe les clients en fonction de la fréquence de leurs achats.

    Monetary Score (Score Monétaire) : Vous attribuez un score monétaire en fonction de la valeur totale dépensée par le client. Le client ayant dépensé le moins reçoit un score de 1, tandis que le client ayant dépensé le plus reçoit un score de 5. Cela classe les clients en fonction du montant total dépensé.

En combinant ces scores, vous obtenez un aperçu global du comportement de chaque client, ce qui facilite la segmentation en différents segments de clients en fonction de leurs scores RFM. Ces scores peuvent ensuite être utilisés pour concevoir des stratégies marketing ciblées pour chaque segment. Le DataFrame rfm contient maintenant ces scores dans les colonnes "recency_score", "frequency_score", et "monetary_score".
# In[17]:


#RFM - La valeur de 2 variables différentes qui ont été formées a été enregistrée sous forme de RFM_SCORE.
rfm["RFM_SCORE"] = (rfm["recency_score"].astype(str) + rfm["frequency_score"].astype(str))


# In[18]:


seg_map = {
    r'[1-2][1-2]': 'hibernating',
    r'[1-2][3-4]': 'at_Risk',
    r'[1-2]5': 'cant_loose',
    r'3[1-2]': 'about_to_sleep',
    r'33': 'need_attention',
    r'[3-4][4-5]': 'loyal_customers',
    r'41': 'promising',
    r'51': 'new_customers',
    r'[4-5][2-3]': 'potential_loyalists',
    r'5[4-5]': 'champions'
}
rfm['segment'] = rfm['RFM_SCORE'].replace(seg_map, regex=True)
rfm.head()


#  r'[1-2][1-2]': 'hibernating' : Les clients dont les scores RFM commencent par 1 ou 2 dans les trois dimensions (Récence, Fréquence, Monétaire) sont étiquetés comme "hibernating", ce qui signifie qu'ils sont inactifs depuis longtemps.
# 
#     r'[1-2][3-4]': 'at_Risk' : Les clients dont les scores RFM commencent par 1 ou 2 dans les deux premières dimensions et par 3 ou 4 dans la dimension Monétaire sont étiquetés comme "at_Risk". Ils présentent un risque de devenir inactifs.
# 
#     r'[1-2]5': 'cant_loose' : Les clients dont les scores RFM commencent par 1 ou 2 dans les deux premières dimensions et se terminent par 5 dans la dimension Monétaire sont étiquetés comme "cant_loose". Cela suggère que ces clients sont précieux et qu'il est important de les retenir.
# 
#     r'3[1-2]': 'about_to_sleep' : Les clients dont les scores RFM commencent par 3 dans la dimension Récence et par 1 ou 2 dans la dimension Fréquence sont étiquetés comme "about_to_sleep". Ils montrent des signes de ralentissement de l'activité d'achat.
# 
#     r'33': 'need_attention' : Les clients dont les scores RFM sont tous les trois égaux à 3 sont étiquetés comme "need_attention". Ils nécessitent une attention particulière car ils sont en train de devenir inactifs.
# 
#     r'[3-4][4-5]': 'loyal_customers' : Les clients dont les scores RFM commencent par 3 ou 4 dans la dimension Récence et se terminent par 4 ou 5 dans la dimension Monétaire sont étiquetés comme "loyal_customers". Ce sont des clients fidèles.
# 
#     r'41': 'promising' : Les clients dont les scores RFM commencent par 4 dans la dimension Récence et par 1 dans la dimension Fréquence sont étiquetés comme "promising". Ils montrent un potentiel de devenir des clients fidèles.
# 
#     r'51': 'new_customers' : Les clients dont les scores RFM commencent par 5 dans la dimension Récence et par 1 dans la dimension Fréquence sont étiquetés comme "new_customers". Ce sont de nouveaux clients.
# 
#     r'[4-5][2-3]': 'potential_loyalists' : Les clients dont les scores RFM commencent par 4 ou 5 dans la dimension Récence et par 2 ou 3 dans la dimension Fréquence sont étiquetés comme "potential_loyalists". Ils ont le potentiel de devenir des clients fidèles.
# 
#     r'5[4-5]': 'champions' : Les clients dont les scores RFM commencent par 5 dans les trois dimensions sont étiquetés comme "champions". Ce sont les clients les plus précieux et les plus actifs.
# 
# Le code rfm['segment'] = rfm['RFM_SCORE'].replace(seg_map, regex=True) applique ces correspondances basées sur les expressions régulières aux scores RFM dans le DataFrame rfm pour attribuer à chaque client un segment en fonction de leurs scores RFM. Cette étape permet de catégoriser les clients en groupes significatifs pour prendre des décisions marketing ciblées.

# In[19]:


#La date du dernier achat du client. La date la plus proche obtient 5 et la date la plus éloignée obtient 1
rfm["recency_score"] = pd.qcut(rfm['Recency'], 5, labels=[5, 4, 3, 2, 1])
# Le nombre total d'achats. La fréquence la moins élevée obtient 1 et la fréquence la plus élevée obtient 5.
rfm["frequency_score"] = pd.qcut(rfm["Frequency"].rank(method="first"), 5, labels=[1, 2, 3, 4, 5])
#Le montant total dépensé par le client. Le moins d'argent obtient 1, le plus d'argent obtient 5.
rfm["monetary_score"]= pd.qcut(rfm["Monetary"],5,labels=[1,2,3,4,5])
rfm.head()


# In[20]:


rfm[["segment", "Recency","Frequency","Monetary"]].groupby("segment").agg(["mean","count","max"]).round()


# In[32]:


plt.figure(figsize=(8, 6))
plt.hist(rfm['Recency'], bins=20, color='skyblue')
plt.title('Distribution de la Récence')
plt.xlabel('Récence (jours)')
plt.ylabel('Nombre de Clients')
plt.show()


# In[33]:


plt.figure(figsize=(8, 6))
plt.hist(rfm['Frequency'], bins=20, color='lightcoral')
plt.title('Distribution de la Fréquence')
plt.xlabel('Fréquence d\'Achat')
plt.ylabel('Nombre de Clients')
plt.show()


# In[34]:


plt.figure(figsize=(8, 6))
plt.hist(rfm['Monetary'], bins=20, color='lightgreen')
plt.title('Distribution de la Valeur Monétaire')
plt.xlabel('Valeur Monétaire (en livres sterling)')
plt.ylabel('Nombre de Clients')
plt.show()


# In[36]:


segment_counts = rfm['segment'].value_counts().sort_index()
plt.figure(figsize=(10, 6))
sns.barplot(x=segment_counts.index, y=segment_counts.values, palette="viridis")
plt.title('Répartition des Clients par Segment RFM')
plt.xlabel('Segment RFM')
plt.ylabel('Nombre de Clients')
plt.xticks(rotation=90)
plt.show()


# # Avis sur les Segments
# 
# Segment "Impossible de Perdre"
# 
#     Nombre de clients dans ce segment : 63.
#     Récence moyenne : 133 jours.
#     Fréquence d'achat moyenne : 8.
#     Nombre total d'achats : 63.
#     Montant total dépensé : 102,54 livres sterling.
# 
# Analyse :
# 
# Même si les clients de ce segment n'ont pas effectué d'achat depuis environ 133 jours, leur fréquence d'achat est remarquablement élevée, avec une moyenne de 8 achats par client. Le nombre total d'achats atteint 63, ce qui indique un fort potentiel de fidélisation de ces clients. Malgré leur absence récente, ils ont déjà démontré un engagement important envers votre entreprise.
# 
# Actions recommandées :
# 
#     Enquêtes de satisfaction : Envoyez des enquêtes de satisfaction à ces clients pour comprendre pourquoi ils ont réduit leur activité. Demandez-leur s'ils ont des préoccupations ou des attentes spécifiques que vous pourriez satisfaire.
# 
#     Campagnes de fidélisation : Créez des campagnes de fidélisation personnalisées par e-mail pour rappeler à ces clients l'existence de votre entreprise et les encourager à revenir. Offrez des incitations spéciales ou des remises pour les réactiver.
# 
#     Offres exclusives : Proposez des offres exclusives ou des avantages spéciaux à ces clients en fonction de leur historique d'achats. Cela peut les inciter à revenir pour effectuer davantage d'achats.
# 
# En mettant en œuvre ces actions, vous pourriez augmenter la rétention de ce segment de clients "Impossible de Perdre" et maximiser leur valeur pour votre entreprise.
#     
#     

# # Besoin d'Attention
# 
# Segment "Besoin d'Attention"
# 
#     Nombre de clients dans ce segment : 187.
#     Récence moyenne : 52 jours.
#     Fréquence d'achat moyenne : 2.
#     Nombre total d'achats : 3.
#     Montant total dépensé : 12 602 livres sterling.
# 
# Analyse :
# 
# Les clients de ce segment ont effectué leurs derniers achats en moyenne il y a 52 jours. Cependant, leur fréquence d'achat est relativement faible, avec une moyenne de 2 achats par client, et un total de 3 achats. Bien que le montant total dépensé soit significatif, il est essentiel de réactiver leur intérêt pour votre marque.
# 
# Actions recommandées :
# 
#     Campagnes de rappel : Envoyez des campagnes de rappel ciblées pour rappeler à ces clients l'existence de votre marque. Mettez en avant les avantages de vos produits ou services et offrez des incitations pour les encourager à revenir.
# 
#     Remises à court terme : Proposez des remises à court terme ou des offres spéciales pour inciter ces clients à effectuer de nouveaux achats rapidement. Cette approche peut être particulièrement efficace pour stimuler les ventes.
# 
#     Personnalisation : Personnalisez vos communications en fonction des préférences de chaque client, en mettant en avant des produits ou des offres susceptibles de les intéresser.
# 
# En mettant en œuvre ces actions, vous pourriez réactiver l'intérêt de ce segment de clients "Besoin d'Attention" et les encourager à revenir et à effectuer davantage d'achats.

# In[ ]:




