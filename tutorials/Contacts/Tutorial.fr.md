 
# Développer l'interface d'une application web monopage avec le *toolkit* *Atlas*

Le *toolkit* *Atlas* permet de programmer des interfaces d'applications web monopages ([SPA](https://en.wikipedia.org/wiki/Single-page_application))). Il est léger (quelques dizaines de Ko), sans dépendances, ne nécessite pas de savoir programmer en *JavaScript* (ou un langage dérivé), et n'impose pas d'architecture logicielle ([*MVC*](https://fr.wikipedia.org/wiki/Mod%C3%A8le-vue-contr%C3%B4leur) ou similaire).

En outre, une application développée avec le *toolkit* *Atlas* est instantanément et automatiquement accessible d'internet, pour peu que l'ordinateur qui l'exécute soit connecté à internet. Tout dispositif équipé d'un navigateur web moderne connecté à internet peut alors y avoir accès, notamment par le biais du [code QR](https://fr.wikipedia.org/wiki/Code_QR) qui s'affiche dans l'application.

Ce document détaille le développement, à l'aide de ce *toolkit*, d'une application basique de gestion de contacts, dont voici un aperçu :

![Apparence de l'application faisant l'objet du tutoriel 'Contacts'](https://q37.info/s/39dr4tcr.png)

L'accent étant mis sur la mise en œuvre de l'*API* du *toolkit* *Atlas*, le lecteur est supposé posséder les connaissances de base nécessaires à la compréhension du code *HTML*/*CSS* et *Python* présent dans ce document. 

Les fichiers source associés à ce document sont disponibles sur *GitHub* (https://github.com/epeios-q37/atlas-python/tree/master/tutorials/Contacts), dépôt lui-même clôné sur *Repl.it* (https://repl.it/@AtlasTK/atlas-python), un *IDE* en ligne.  
Si vous avez *Python* 3 d'installé sur votre ordinateur, vous pouvez récupérer le dépôt *GitHub* et visualiser/exécuter directement sur votre machine le code associé aux différentes sections de ce document.
Vous pouvez également, notamment si vous n'avez pas *Python* 3 d'installé, visualiser/exécuter ce code directement dans votre navigateur, en utilisant le lien *Repl.it* ci-dessus.

Pour ne pas allonger outre mesure ce document, chaque section ne contiendra que les parties du code qui la concerne. Néanmoins, au début de chaque section, il y aura un lien vers le code source complet tel que décrit dans cette section, ainsi que les instructions à lancer pour l'exécuter sur *Repl.it* et en local.

Les lignes, dans les fichiers source, précédant la ligne `import atlastk` ne sont là que pour faciliter l'utilisation de ces fichiers dans le cadre de ce document et ne sont pas nécessaires à une utilisation courante du *toolkit* *Atlas*.


## Le ficher *HTML* principal (`Main.html`)

> Code source : <https://github.com/epeios-q37/atlas-python/blob/master/tutorials/Contacts/Main.html>.

Le fichier `Main.html` est un fichier au format *HTML* décrivant l'interface.  
Ce fichier va prendre place dans la section *body* de la page *HTML* constituant l'interface de l'application

### Structure générale

Voici le contenu partiel de ce fichier, reflétant sa structure générale :

```html
<fieldset>
  <fieldset id="Contact">
    <!-- Détail d'un contact -->
  </fieldset>
  <div style="display: table; margin: 10px auto auto auto;">
    <div>
      <!-- Boutons généraux. -->  
    </div>
    <div class="Edition">
      <!-- Boutons de saisie.-->
    </div>
  </div>
</fieldset>
<div style="display: table; margin: 10px auto auto auto; border-collapse: collapse;">
  <!-- Liste des contacts -->
</div>
```

Il est aisément compréhensible pour ceux qui sont familiers avec *HTML*.

Ses différentes sous-parties vont être détaillées ci-dessous.

### Détail d'un contact

Voici le code dédié à l'affichage du détail d'un contact :

```html
<table style="margin: auto;">
  <tr>
    <td>
      <label for="Name">Full name:</label>
    </td>
    <td>
      <input id="Name" size="50" />
    </td>
  </tr>
  <tr>
    <td>
      <label for="Address">Address:</label>
    </td>
    <td>
      <input id="Address" size="50" />
    </td>
  </tr>
  <tr>
    <td>
      <label for="Phone">Phone:</label>
    </td>
    <td>
      <input id="Phone" type="tel" size="50" />
    </td>
  </tr>
  <tr>
    <td>
      <label for="Note">Note:</label>
    </td>
    <td>
      <textarea id="Note" style="width: 100%;"></textarea>
    </td>
  </tr>
</table>
```

On y trouve un tableau, avec, pour chaque ligne, un des champs constituant un contact, accompagné d'un libellé et d'un identifiant explicite.

### Boutons généraux

Ces boutons vont servir à créer/éditer/supprimer un contact.  
En voici le code :

```html
<button class="Display" data-xdh-onevent="New">New</button>
<span class="DisplayAndSelect">
  <button data-xdh-onevent="Edit">Edit</button>
  <button data-xdh-onevent="Delete">Delete</button>
</span>
```

À part l'attribut `data-xdh-onevent`, on n'a là que du *HTML* des plus classiques.  
Les différentes classes (`Display` et `DisplayAndSelect`) ont cependant un rôle bien particulier, qui sera révélé dans les sections qui suivent.

L'attribut `data-xdh-onevent` prend ici la place de l'habituel attribut `onclick`. L'attribut `onclick` prend habituellement pour valeur le code *JavaScript* à lancer lorsque l'on clique sur le bouton auquel il est affecté.  
Ici, à la place, on utilise l'attribut `data-xdh-onevent` qui va prendre pour valeur un libellé d'action, libellé que l'on retrouvera dans le code *Python*. On va pouvoir ainsi coder les actions à réaliser lors d'un clic sur le bouton non plus en *JavaScript*, mais en *Python*.

### Boutons de saisie

Ces boutons sont affichés lors de la saisie d'un contact, et permettent de valider ou d'annuler cette saisie.  
Voici le code correspondant :

```html
<button data-xdh-onevent="Cancel">Cancel</button>
<button data-xdh-onevent="Submit">Submit</button>
```

Là encore, rien de particulier, mis à part l'attribut `data-xdh-onevent`, que l'on a déjà rencontré ci-dessus.  
Le contenu des attributs `data-xdh-onevent`, à savoir `Cancel` et `Submit`, va être utilisé dans le code *Python* de l'application.   
Notez que le nom du bouton (la valeur de l'élément `button`) est identique à la valeur de son attribut `data-xdh-onevent` uniquement par commodité ; ce n'est en rien obligatoire.

### Liste de contacts

Cette partie affiche le tableau qui va accueillir la liste des contacts au sein de son élément `tbody`, dont le contenu va être généré par l'application.  
En voici le contenu :

```html
<table id="Contacts" style="cursor: default; border-collapse: collapse;">
  <thead>
    <th>Name</th>
    <th>Address</th>
    <th>Phone</th>
    <th>Note</th>
  </thead>
  <tbody id="Content" />
</table>
```

Notez l'identifiant `Content`, que l'on va retrouver dans le code *Python*. L'identifiant `Contacts` n'est utilisé que dans le fichier `Head.html` décrit ci-dessous.

## Le fichier des métadonnées (`Head.html`)

> Code source : <https://github.com/epeios-q37/atlas-python/blob/master/tutorials/Contacts/Head.html>.


Ce fichier, également au format *HTML*,  prendra place dans la section *head* de la page *HTML* constituant l'interface de l'application.

### Apparence de l'application

La première partie de ce fichier définit le titre, l'icône, et, à l'aide de quelques règles *CSS*, diverses retouches au niveau de l'apparence de l'interface.

En voici le contenu :

```html
<title>Address book</title>
<link rel="icon" type="image/png"
	href="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgBAMAAACBVGfHAAAAMFBMVEUEAvyEhsxERuS8urQsKuycnsRkYtzc2qwUFvRUVtysrrx0ctTs6qTMyrSUksQ0NuyciPBdAAABHklEQVR42mNgwAa8zlxjDd2A4POfOXPmzZkFCAH2M8fNzyALzDlzg2ENssCbMwkMOsgCa858YOjBKxBzRoHhD7LAHiBH5swCT9HQ6A9ggZ4zp7YCrV0DdM6pBpAAG5Blc2aBDZA68wCsZPuZU0BDH07xvHOmAGKKvgMP2NA/Zw7ADIYJXGDgLQeBBSCBFu0aoAPYQUadMQAJAE29zwAVWMCWpgB08ZnDQGsbGhpsgCqBQHNfzRkDEIPlzFmo0T5nzoMovjPHoAK8Zw5BnA5yDosDSAVYQOYMKIDZzkoDzagAsjhqzjRAfXTmzAQgi/vMQZA6pjtAvhEk0E+ATWRRm6YBZuScCUCNN5szH1D4TGdOoSrggtiNAH3vBBjwAQCglIrSZkf1MQAAAABJRU5ErkJggg==" />
<style>
	#Contact label {
		font-weight: bold;
	}

	#Contact span {
		text-align: left;
	}

	#Contacts th,
	#Contacts td {
		border: 1px solid black;
		padding: 0% 5px;
	}

	#Contacts td:nth-child(3) {
		text-align: right;
	}

	#Contacts tr:nth-child(even)
	{
		background: #CCC
	}

	#Contacts tr:nth-child(odd)
	{
		background: #FFF
	}

	#Contact *:disabled {
		background-color: snow;
		color: initial;
	}
</style>
```

### Visibilité des boutons

La seconde partie du fichier permet de gérer la visibilité des boutons.

En voici le contenu :

```html
<style id="HideDisplay">
	.Display {
		display: none;
	}
</style>
<style id="HideDisplayAndSelect">
	.DisplayAndSelect {
		display: none;
	}
</style>
<style id="HideEdition">
	.Edition {
		display: none;
	}
</style>
```

On y voit des éléments `style` accompagnés d'un identifiant. Ces éléments vont permettre de cacher/afficher certains boutons.  
En effet, chaque élément `style` définit une règle pour une certaine classe. En activant/désactivant un de ces éléments, on ajoute/retire à cette classe la règle *CSS* contenu dans l'élément. Par conséquent, on agit ainsi sur les éléments, en l'occurrence des boutons, auxquels cette classe est affectée.

On retrouvera les différents identifiants de ces éléments `style` dans le code détaillé dans les sections qui suivent.

## Rendu de l'interface (`part1.py`)

> * Code source : <https://github.com/epeios-q37/atlas-python/blob/master/tutorials/Contacts/part1.py> ;
> * exécution :
>   * sur [*Repl.it*](https://repl.it/@AtlasTK/atlas-python) : bouton *Run*, `m1` + *entrée*, clic sur URL,
>   * en local : `python3 atlas-python/tutorials/Contacts/part1.py`

On va ici afficher l'interface de l'application, dont, suite à une action de l'utilisateur, seules les parties qui le nécessitent seront modifiées.

### Affichage de la page *HTML*

En premier lieu, on va définir la fonction qui sera appelée à chaque ouverture de session :

```python
def ac_connect(dom):
  dom.inner("",open("Main.html").read())
```

`dom` est un objet fournit par le *toolkit* *Atlas* ; chaque session a sa propre instance de cet objet.

Dans cette fonction, la méthode `inner(…)`va remplacer la totalité de la page web par le contenu du fichier `Main.html` précédemment décrit.  
Le premier paramètre de cette méthode est l'identifiant de l'élément dont on va remplacer le contenu. La chaîne vide est une valeur spéciale qui fait référence à l'élément racine de la page.  
À titre indicatif, il existe également les méthodes `before(…)`, `begin(…)`, `end(…)` et `after(…)` pour insérer le contenu respectivement juste avant, au début, à la fin ou juste après l’élément dont l'identifiant est passé en paramètre.

On va ensuite affecter cette fonction à une action, à l'aide d'un dictionnaire nommé, par convention, `CALLBACKS` :

```python
CALLBACKS = {
  "": ac_connect
 }
```

Ici, `ac_connect` est affecté à une action dont le libellé est une chaîne vide. Cette valeur correspond à l'action qui est lancée à chaque nouvelle session.

### La boucle évènementielle

On va ensuite lancer la boucle évènementielle de l'application, en lui passant le dictionnaire des actions, ainsi que le contenu du fichier `Head.html` décrit précédemment :

```python
atlastk.launch(CALLBACKS,None,open("Head.html").read())
```

Le paramètre dont la valeur est `None` sera abordé plus tard.

## Liste des contacts (`part2.py`)

> * Code source : <https://github.com/epeios-q37/atlas-python/blob/master/tutorials/Contacts/part2.py> ;
> * exécution :
>   * sur [*Repl.it*](https://repl.it/@AtlasTK/atlas-python) : bouton *Run*, `m2` + *entrée*, clic sur URL,
>   * en local : `python3 atlas-python/tutorials/Contacts/part2.py`

Dans cette section, nous allons programmer l'affichage de la liste des contacts.

### Liste fictive

On va d'abord créer une liste de contacts fictives, histoire d'avoir quelque chose à afficher :

```python
EXAMPLE = [
  {
    "Name": "Holmes, Sherlock",
    "Address": "221B Baker Street, Londres",
    "Phone": "(use telegraph)",
    "Note": "Great detective!"
  },
  {
    "Name": "Holmes, Mycroft",
    "Address": "Diogenes Club, Pall Mall, Londres",
    "Phone": "(use telegraph)",
    "Note": "Works for the British government.\nBrother of Holmes, Sherlock."
  },
  {
    "Name": "Tintin",
    "Address": "Château de Moulinsart",
    "Phone": "421",
    "Note": "Has a dog named Snowy."
  },
  {
    "Name": "Tournesol, Tryphon (prof.)",
    "Address": "Château de Moulinsart",
    "Phone": "421",
    "Note": "Creator of the Bianca rose."
  }
]
```

On va affecter cette liste à une variable qui fera office de base de données :

```python
contacts = EXAMPLE
```

### Affichage

Créons une fonction dédiée à l'affichage de cette liste :

```python
def display_contacts(dom):
  html = ""

  for contactId in range(len(contacts)):
    contact = contacts[contactId]
    html += f'<tr id="{contactId}" data-xdh-onevent="Select" style="cursor: pointer;">'
    for key in contact:
      html += f'<td>{contact[key]}</td>'
    html += '</td>'

  dom.inner("Content", html)
```

Dans cette fonction, on récupère chaque contact de la liste, et, pour chacun de ces contacts, le contenu de chacun de ses champs. On va s'en servir pour créer le contenu du corps du tableau dédié à l'affichage de la liste, qui sera stocké dans la variable `html`.  
Le contenu de cette variable est ensuite injecté dans le corps de la table, plus précisément dans l'élément `tbody` d'identifiant `Content` (voir le fichier `Main.html`), grâce à la méthode `inner(…)`, que l'on a déjà rencontré. Notez que le premier paramètre n'est plus une chaîne de caractères vide, mais bien l'identifiant de l'élément concerné (`Content`).  
Chaque ligne du tableau a son propre identifiant, et un attribut `data-xdh-onevent="Select"` qui fera l'objet de la prochaine section.

Enfin, on ajoute l'appel à cette fonction dans la fonction `ac_connect(…)`, :

```python
def ac_connect(dom):
  dom.inner("",open("Main.html").read())
  display_contacts(dom)
```

## Détail d'un contact (`part3.py`)

> * Code source : <https://github.com/epeios-q37/atlas-python/blob/master/tutorials/Contacts/part3.py> ;
> * exécution :
>   * sur [*Repl.it*](https://repl.it/@AtlasTK/atlas-python) : bouton *Run*, `m3` + *entrée*, clic sur URL,
>   * en local : `python3 atlas-python/tutorials/Contacts/part3.py`

Procédons maintenant à l'affichage des détails d'un contact sélectionné par l'utilisateur.

### Fonction générale d'affichage

On va commencer par le remplissage des champs au sommet de l'interface avec les valeurs du contact sélectionné dans la liste.

Voici la fonction correspondante :

```python
def display_contact(contactId,dom):
  dom.set_values(contacts[contactId])
```

La méthode `set_values(…)` prend un dictionnaire avec, pour clefs, des identifiants d'éléments, et, pour valeurs, le contenu que doivent prendre ces éléments.  
Comme, dans la page *HTML*, les identifiants des éléments sont identiques aux clefs correspondants aux champs d'un contact, le dictionnaire est déjà constitué et n'est plus à construire. On l'utilise donc tel quel dans l'appel de la méthode `set_values(…)`.  
`contactId` est l'index, dans la liste `contacts`, du contact à afficher. 

### Sélection d'un contact

On va maintenant définir la fonction que l'on va affecter à l'action `Select` définit dans l'attribut `data-xdh-onevent` du code *HTML* qui est crée dans la précédente section :

```python
def ac_select(dom,id):
  display_contact(int(id),dom)
```

Le paramètre `id` contient l'identifiant de l'élément recevant l'évènement à l'origine de l'action à laquelle cette fonction a été affectée. Ici, l'évènement est un clic sur une ligne du tableau contenant la liste des contacts, évènement auquel a été associée l'action `Select` via l'attribut `data-xdh-onevent`. Conformément à ce qui va être défini ci-dessous dans la variable `CALLBACKS`, cette action va lancer la fonction `ac_select`.

Dans la section précédente, on a vu que, pour le tableau *HTML* contenant la liste des contacts, chaque ligne a pour identifiant l'index, dans la table `contacts`, du contact correspondant. On peut donc utiliser directement `id`, après l'avoir convertit en entier (`id` est fourni sous forme d'une chaîne de caractères), pour le passer à la fonction `display_contact(…)`

On met à jour la table `CALLBACKS`, en affectant cette fonction à l'action `Select` (définie comme valeur de l'attribut `data-xdh-onevent` dans le code *HTML* généré dans la précédente section) :

```python
CALLBACKS = {
  …
  "Select": ac_select
}
```

## Désactivation des champs + bouton *New* (`part4.py`)

> * Code source : <https://github.com/epeios-q37/atlas-python/blob/master/tutorials/Contacts/part4.py> ;
> * exécution :
>   * sur [*Repl.it*](https://repl.it/@AtlasTK/atlas-python) : bouton *Run*, `m4` + *entrée*, clic sur URL,
>   * en local : `python3 atlas-python/tutorials/Contacts/part4.py`

On remarquera que le contenu des champs dans lesquels s'affichent les détails sont modifiables, ce qui n'est pas le comportement voulu dans ce contexte. On va donc écrire le code permettant de désactiver ces champs.

### Champs à désactiver

Pour cela, on va d'abord créer une liste contenant les identifiants des différents  champs à désactiver :

```python
FIELDS = [
  "Name",
  "Address",
  "Phone",
  "Note"
]
 ```

### Gestion générale des éléments interactifs

 On va créer une fonction qui va gérer l'état de ces champs, et qui sera complétée ultérieurement pour gérer d'autre éléments :

 ```python
def update_outfit(dom):
  dom.disable_elements(FIELDS)
 ```

Cette fonction fait appel à la méthode `disable_elements(…)`, dont le rôle est de désactiver les éléments dont les identifiants sont passés en paramètres.

On va également utiliser cette fonction pour faire apparaître le bouton *New*, qui permet de saisir un nouveau contact.  
La classe `Display` étant affectée à ce bouton (voir le fichier `Main.html`), on va désactiver l'élément `style` d'identifiant `HideDisplay` (voir le fichier `Head.html`) qui définit la règle cachant les éléments de la classe, en utilisant la méthode `disable_element` (notez l'absence du `s` final). La fonction `update_outfit(…)` se présente alors de la manière suivante :

```python
def update_outfit(dom):
  dom.disable_elements(FIELDS)
  dom.disable_element("HideDisplay")
```

On pourrait également ajouter l'identifiant `HideDisplay` à la liste passée à `disable_elements(…)`, pour économiser un appel de fonction. 
 
### Mise en œuvre

 On va appeler cette fonction à chaque action de l'utilisateur, ce qui peut sembler ne pas être approprié vu son contenu, mais c'est en prévision de ce qu'elle contiendra une fois qu'elle sera enrichie dans les sections suivantes :

```python
def ac_connect(dom):
  dom.inner("",open("Main.html").read())
  display_contacts(dom)
  update_outfit(dom)

def ac_select(dom,id):
  display_contact(int(id),dom)  
  update_outfit(dom)
```

## Saisie d'un nouveau contact (`part5.py`)

> * Code source : <https://github.com/epeios-q37/atlas-python/blob/master/tutorials/Contacts/part5.py> ;
> * exécution :
>   * sur [*Repl.it*](https://repl.it/@AtlasTK/atlas-python) : bouton *Run*, `m5` + *entrée*, clic sur URL,
>   * en local : `python3 atlas-python/tutorials/Contacts/part5.py`

On va maintenant gérer l'action affectée au bouton *New*. Pour cela, on va utiliser un objet qui va stocker dans quel mode est placé le logiciel, à savoir *édition* ou *affichage*.

### Les différents états de l'application

On va d'abord crée un *enum* relatifs à ces deux états, à l'aide du module *enum*, que l'on va importer en modifiant l'instruction d'importation existante :

```python
 import atlastk, enum
```

Créons l'*enum* proprement dit :

```python
class State(enum.Enum):
  DISPLAY = enum.auto()
  EDIT = enum.auto()
```

### Classe dédiée à chaque session

On va maintenant créer une classe `Board` dans laquelle on va stocker les différentes variables propres à chaque session :

```python
class Board:
  def __init__(self):
    self.state = State.DISPLAY
```

Le constructeur de cette classe (`__init__(…)`) va stocker l'état initial de l'application, à savoir `DISPLAY` (affichage), dans la variable membre `state`.

Il faudra créer une instance de cette classe pour chaque nouvelle session. Ceci est realisé automatiquement par le *toolkit* *Atlas* : il suffit de modifier l'appel à la fonction fonction `launch(…)` en remplaçant le paramètre de valeur `None` par le constructeur de cette classe, ce qui donne :

```python
atlastk.launch(CALLBACKS,Board,open("Head.html").read())
```

Ce faisant, toutes les fonctions référencées dans `CALLBACKS`, qui, je le rappelle, associe fonctions et actions, vont recevoir l'instance de l'objet `Board` correspondant à la session à l'origine de l'appel. Il faut donc modifier le prototype de ces fonctions :

```python
def ac_connect(board,dom):
  …

def ac_select(board,dom,id):
  …
```

Notez l'ajout du paramètre `board`.

### Adaptation de la gestion des contrôles interactifs

On va passer ce paramètre à la fonction `update_outfit(…)`, pour qu'on puisse y tenir compte de l'état dans lequel se trouve l'application et agir en conséquence, ce qui donne :

```python
def update_outfit(board,dom):
  if board.state == State.DISPLAY:
    dom.disable_elements(FIELDS)
    dom.disable_element("HideDisplay")
  elif board.state == State.EDIT:
    dom.enable_elements(FIELDS)
    dom.enable_elements("HideDisplay")
```

On voit l'apparition des méthodes `enable_element[s](…)`, qui sont les pendants des méthodes `disable_element[s](…)`.

### Autres adaptations

Il faut, bien entendu, également modifier les appels à `update_outfit(…)` en conséquence ; on va également, par précaution, mettre à jour, dans l'instance `board`, l'état de l'application pour être sûr qu'il correspond à l'action lancée :

```python
def ac_connect(board,dom):
  …
  board.state = State.DISPLAY
  update_outfit(board,dom)


def ac_select(board,dom,id):
  …
  board.state = State.DISPLAY
  update_outfit(board,dom)
```

On va également modifier la fonction `display_contact(…)`, pour pouvoir l'utiliser afin de vider le contenu des champs. Pour cela on va créer un dictionnaire correspondant à un contact vide :

```python
EMPTY_CONTACT = {
  "Name": "",
  "Address": "",
  "Phone": "",
  "Note": ""
}
```

qui va être utilisé de la manière suivante dans la fonction `display_contact(…)` :

```python
def display_contact(contactId,dom):
  dom.set_values(EMPTY_CONTACT if contactId == None else contacts[contactId])
```

On notera que donner la valeur `None` au paramètre `contactId` entraînera dorénavant le vidage des champs.

### Activation de la saisie

Ne reste plus qu'à définir la fonction qui sera appelée lors d'un clic sur le bouton *New* :

```python
def ac_new(board,dom):
  board.state = State.EDIT
  display_contact(None,dom)
  update_outfit(board,dom)
  dom.focus("Name")
```

Cette fonction réalise successivement les opérations suivantes :
- stockage dans l'instance de l'objet `board` du nouvel état du logiciel, à savoir `EDIT` (édition) ;
- vidage des champs de saisie ;
- mise à jour de l'apparence de l'interface ;
- affectation du focus (méthode `focus(…)`) au premier champs éditable (d'identifiant `Name`, qui correspond au nom du contact), de manière à ce que l'utilisateur puisse procéder immédiatement à la saisie du nouveau contact.

N'oublions pas de l'associer à l'action idoine :

```python
CALLBACKS = {
  …
  "New": ac_new
 }
 ```

## Boutons de saisie (`part6.py`)

> * Code source : <https://github.com/epeios-q37/atlas-python/blob/master/tutorials/Contacts/part6.py> ;
> * exécution :
>   * sur [*Repl.it*](https://repl.it/@AtlasTK/atlas-python) : bouton *Run*, `m6` + *entrée*, clic sur URL,
>   * en local : `python3 atlas-python/tutorials/Contacts/part6.py`

On peut maintenant saisir un nouveau contact, mais il manque les boutons pour valider ou annuler cette saisie.

### Adaptation de la gestion des contrôles interactifs

Pour afficher les boutons *Submit* et *Cancel*, on va désactiver l'élément `style` d'identifiant `HideEdition` (dans le fichier `Head.html`). Cet élément définit une règle cachant les éléments auxquels on a affecté la classe `Edition`. C'est le cas de l'élément `div` qui contient les deux boutons d'édition `Submit` et `Cancel` (voir le fichier `Main.html`).  
Désactiver ce style pour faire apparaître les boutons d'éditions ne suffit pas ; il faut également l'activer pour cacher ces boutons lorsque requis. On va, pour cela, modifier la fonction `update_outfit(…)` afin d'obtenir cela :

```python
def update_outfit(board,dom):
  if board.state == State.DISPLAY:
    dom.disable_elements(FIELDS)
    dom.disable_element("HideDisplay")
    dom.enable_element("HideEdition")
  elif board.state == State.EDIT:
    dom.enable_elements(FIELDS)
    dom.enable_element("HideDisplay")
    dom.disable_element("HideEdition")
```

### Confirmation/annulation d'une saisie

Maintenant que les boutons sont affichés, on va créer les fonctions associées.

Pour le bouton *Cancel*, on va demander confirmation et, en fonction de la réponse, ne rien faire, ou repasser en mode d'affichage après avoir vider les champs de saisie :

```python
def ac_cancel(board,dom):
  if dom.confirm("Are you sure?"):
    display_contact(None,dom)
    board.state = State.DISPLAY
    update_outfit(board,dom)
```

La méthode `confirm(…)` ouvre une boîte de dialogue affichant la chaîne de caractère passée en paramètre. Elle retourne `True` lorsque l'on clique sur le bouton *OK* (ou ce qui en tient lieu), ou `False` si on clique sur le bouton *Cancel* (ou ce qui en tient lieu), tout en fermant ladite boîte de dialogue.

Pour le bouton `Submit`, il s'agit de récupérer les valeurs des champs de saisie, de stocker lesdites valeurs dans ce qui tient lieu de base de donnée, à savoir la variable `contacts`, de rafraîchir la liste des contacts, et de rebasculer en mode saisie, tout cela sous condition que le champs `Name` contienne une valeur :

```python
def ac_submit(board,dom):
  idsAndValues = dom.get_values(FIELDS)

  if not idsAndValues['Name'].strip():
    dom.alert("The name field can not be empty!")
  else:
    board.state = State.DISPLAY
    contacts.append(idsAndValues)
    display_contact(None,dom)
    display_contacts(dom)
    update_outfit(board,dom)
```

La méthode `get_values(…)` prend une liste de chaînes de caractères correspondants à des identifiants d'éléments, et retourne un dictionnaire avec, pour clefs, ces identifiants, et, pour valeurs, le contenu de ces éléments. Comme les identifiants sont identiques aux clefs d'un contact, ou peut stocker le dictionnaire obtenu tel quel.

La méthode `alert(…)` affiche simplement une boîte de dialogue contenant, comme message, la chaîne passée en paramètre, avec un bouton *OK* (ou équivalent) permettant de la fermer.

On termine en mettant à jour `CALLBACKS` pour affecter ces nouvelles fonctions aux actions adéquates :

```python
CALLBACKS = {
  …
  "Cancel": ac_cancel,
  "Submit": ac_submit
}
```

## Les autres boutons (`part7.py`)

> * Code source : <https://github.com/epeios-q37/atlas-python/blob/master/tutorials/Contacts/part7.py> ;
> * exécution :
>   * sur [*Repl.it*](https://repl.it/@AtlasTK/atlas-python) : bouton *Run*, `m7` + *entrée*, clic sur URL,
>   * en local : `python3 atlas-python/tutorials/Contacts/part7.py`

Il nous reste deux boutons à gérer : le bouton d'édition (*Edit*) et le bouton de suppression (*Delete*).

### Adaptation de la classe `Board`

Avant toute chose, nous allons modifier la classe `Board` pour lui ajouter une variable (`contactId`) stockant l'index, dans la liste, du contact sélectionné. Cette variable est mise à `None` lorsqu'aucun contact n'est sélectionné :

```python
class Board:
  def __init__(self):
    self.state = State.DISPLAY
    self.contactId = None
```

Nous allons également modifier `ac_select(…)` pour gérer cette nouvelle variable :

```python
def ac_select(board,dom,id):
  board.contactId = int(id)
  display_contact(board.contactId,dom)  
  …
```

### Adaptation de la gestion des contrôles interactifs

La variable ajoutée à la classe `Board` va également nous servir pour l'affichage des boutons manquants.  
La classe `DisplayAndSelect` est affectée à ces boutons (voir le fichier `Main.html`), dont la règle *CSS* pour cacher les éléments de cette classe est définie dans l'élément `style` d'identifiant `HideDisplayAndSelect` (voir le fichier `Head.html`).

On obtient donc cela :

```python
def update_outfit(board,dom):
  if board.state == State.DISPLAY:
    …
    if board.contactId == None:
      dom.enable_element("HideDisplayAndSelect")
    else:
      dom.disable_element("HideDisplayAndSelect")
  elif board.state == State.EDIT:
    …
    dom.enable_elements(("HideDisplay","HideDisplayAndSelect"))
    …
```

### Modification d'un contact

Passons à la fonction qui sera associée au bouton *Edit*. Elle reprendra en grande partie le contenu de la fonction `ac_new(…)` (on pourrait d'ailleurs en factoriser une partie) :

```python
def ac_edit(board,dom):
  board.state = State.EDIT
  display_contact(board.contactId,dom)
  update_outfit(board,dom)
  dom.focus("Name")
```

Il faut aussi modifier la fonction `ac_submit(…)`, pour tenir compte de son exécution dans le cadre de la modification d'un contact :

```python
def ac_submit(board,dom):
  …
  else:
    board.state = State.DISPLAY
    if board.contactId == None:
      contacts.append(idsAndValues)
    else:
      contacts[board.contactId] = idsAndValues
    display_contact(board.contactId,dom)
    display_contacts(dom)
    …
```

Et également la fonction `ac_cancel(…)` pour la même raison : 

```python
  if dom.confirm("Are you sure?"):
    display_contact(board.contactId,dom)
    board.state = State.DISPLAY
    update_outfit(board,dom)
```

Et mettons à jour `CALLBACKS` :

```python
CALLBACKS {
  …
  "Edit": ac_edit
}
```

### Suppression d'un contact

Implémentons maintenant la fonction qui sera associée au bouton *Delete*, qui ne présente rien de particulier, au regard de ce qui a été abordé dans les précédentes sections :

```python
def ac_delete(board,dom):
  contacts.pop(board.contactId)
  board.contactId = None;
  display_contact(None,dom)
  display_contacts(dom)
  update_outfit(board,dom)
```

Et mettons à jour `CALLBACKS` :

```python
CALLBACKS {
  …
  "Delete": ac_delete
}
```

## Bonus (`part8.py`)

> * Code source : <https://github.com/epeios-q37/atlas-python/blob/master/tutorials/Contacts/part8.py> ;
> * exécution :
>   * sur [*Repl.it*](https://repl.it/@AtlasTK/atlas-python) : bouton *Run*, `m8` + *entrée*, clic sur URL,
>   * en local : `python3 atlas-python/tutorials/Contacts/part8.py`

Comme vous avez pu le constater, la variable `contacts` est globale. Cela a pour conséquence qu'elle est commune à toutes les sessions. Cependant, une modification apportée à cette variable par une session n'est pas immédiatement visible dans toutes les sessions.  
L'objet de cette section est d'apporter les modifications au code pour remédier à cela.

On va se limiter à rafraîchir, dés qu'une modification y est apportée, la liste des contacts dans l'ensemble des sessions.

Pour commencer, on va créer une fonction qui va rafraîchir la liste des contacts :

```python
def ac_refresh(board,dom):
  display_contacts(dom)
```

Elle présente des similitudes, concernant les paramètres qu'elle reçoit, avec les fonctions associées à des actions (`ac_edit(…)`, `ac_submit(…)`…). Cela n'a rien d'étonnant, car on va effectivement l'associer à une action :

```python
CALLBACKS = {
  …
  "Refresh": ac_refresh
}
```

Et maintenant, on va remplacer, dans les fonctions qui modifient la liste des contacts, à savoir `ac_submit(…)` et `ac_delete(…)`, chaque appel à la fonction `display_contacts(dom)` par un appel à `atlastk.broadcast_action("Refresh")`.

```python
def ac_submit(board,dom):
  …
    display_contact(board.contactId,dom)
    atlastk.broadcast_action("Refresh")
    update_outfit(board,dom)


def ac_delete(board,dom):
  …
  display_contact(None,dom)
  atlastk.broadcast_action("Refresh")
  update_outfit(board,dom) 

```

`atlastk.broadcast_action(…)` lance l'action dont le libellé est passé en paramètre dans toutes les sessions, ce qui, en l'occurrence, va provoquer l'appel à la fonction `display_contacts(…)`, et ainsi la liste des contacts sera rafraîchie dans toutes les sessions.

Le fait que la variable `contacts` soit globale, et donc modifiable par toute les sessions, nécessiterait d'écrire du code supplémentaire, notamment pour en contrôler l'accès. De par l'absence de ce code, il est facile de mettre cette application en défaut. Néanmoins, ce code ne concernant pas directement le *toolkit* *Atlas*, il sort du cadre de ce document, et ne sera donc pas abordé ici.


