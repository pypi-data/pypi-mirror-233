# Client Python pour la banque Crédit agricole - Particuliers

![](https://github.com/dmachard/creditagricole_particuliers/workflows/Publish%20to%20PyPI/badge.svg)

Ce client Python est à destination des particuliers souhaitant récupérer ses opérations bancaires stockées par le Crédit Agricole.

## Installation

```python
pip install creditagricole_particuliers
```
  
## Authentification

Paramètres pour l'authentification:
- `username` (string): votre numéro de compte bancaire 
- `password` (list of integer): votre mot de passe
- `department` (integer): numéro de département de votre caisse régionale

```python
from creditagricole_particuliers import Authenticator

session = Authenticator(username="01234567890", 
                        password=[1, 2, 3, 4, 5, 6], 
                        department=999)
```

## Lister l'ensemble des comptes bancaires

```python
from creditagricole_particuliers import Accounts

accounts = Accounts(session=session)
for acc in accounts:
    print(acc)
```

Output:

```
Compte[numero=xxxxxxxxxxx, produit=Compte de Dépôt]
Compte[numero=xxxxxxxxxxx, produit=Livret A]
Compte[numero=xxxxxxxxxxx, produit=Livret Tiwi]
```

Format JSON:

```python
accounts = Accounts(session=session)
print(accounts.as_json())
```

## Rechercher un compte bancaire

```python
from creditagricole_particuliers import Accounts

account = Accounts(session=session).search(num="<n° de compte bancaire>")
print(account)
```

Format JSON:

```python
account = Accounts(session=session).search(num="<n° de compte bancaire>")
print(account.as_json())
```

## Récupération du solde d'un compte


```python
from creditagricole_particuliers import Accounts

account = Accounts(session=session).search(num="<n° de compte bancaire>")
print(account.get_solde())
```

exemple pour la totalité des comptes


```python
from creditagricole_particuliers import Accounts

solde = Accounts(session=session).get_solde()
print(solde)
```

## Récupération des opérations bancaires

Exemple pour récupérer les 30 dernières opérations

```python
from creditagricole_particuliers import Accounts

# search account
account = Accounts(session=session).search(num="<n° de compte bancaire>")

# get operations
operations = account.get_operations(count=30)
for op in operations:
    print(op)
```

Output:

```
Operation[date=Dec 31, 2020 12:00:00 AM, libellé=DE L'ANNEE TAUX  0,500%, montant=0.00]
Operation[date=Dec 31, 2020 12:00:00 AM, libellé=DE L'ANNEE TAUX  0,750%, montant=0.00]

```


Format JSON et filtrage par date

```python
account = Accounts(session=session).search(num="<n° de compte bancaire>")
operations = account.get_operations(date_start="2021-06-15", date_stop="2021-06-30", count=30)
print(operations.as_json())
```

## Lister les cartes bancaires

```python
from creditagricole_particuliers import Cards

cards = Cards(session=session)
for cb in cards:
    print(cb)
```

Output:

```bash
Carte[compte=xxxxxxxxxx, type=MCD, titulaire=xxxxxxxxxxx]
Carte[compte=xxxxxxxxxx, type=Mastercard sans contact débit immédiat, titulaire=xxxxxxxxxxxxx]
```

Format JSON:

```python
cards = Cards(session=session)
print(cards.as_json())
```

## Rechercher une carte bancaire

```python
from creditagricole_particuliers import Cards

cb = Cards(session=session).search(num_last_digits="<4 derniers chiffres de votre carte bancaire>")
print(cb)
```

## Récupération des opérations pour une carte bancaire à débit différé

```python
from creditagricole_particuliers import Cards

# search account
cb = Cards(session=session).search(num_last_digits="<4 derniers chiffres de votre carte bancaire>")

# get operations
operations = cb.get_operations()
for op in operations:
    print(op)
```

## Récupération du code IBAN d'un compte

```python
from creditagricole_particuliers import Accounts

account = Accounts(session=session).search(num="xxxxxxxxxx")
print(account.get_iban())
```

Output:

```bash
Iban[compte=xxxxx, code=FRxxxxxxxxxxxxxxxxxxxxxxxx]
```

Format JSON:

```python
account = Accounts(session=session).search(num="xxxxxxxxxx")
iban = account.get_iban()
print(iban.as_json())
```
