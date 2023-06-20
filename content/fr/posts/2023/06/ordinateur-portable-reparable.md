---
title: |
  À la recherche d'un ordinateur portable réparable
description: |
  Ça y est, mon fidèle MacBook Pro mi-2012 est définitivement obsolète. J'explique dans ce billet ma recherche d'un ordinateur portable réparable pour le remplacer. Où l'on finit par traîner du côté du Framework Laptop et du fabricant why!…
date: "2023-06-20"
category: retrospectives
tags:
  - numerique-responsable
  - logiciels-libres
image: "/static/img/articles/ordinateur-portable-reparable.jpg"
image_thumbnail: "/static/img/articles/ordinateur-portable-reparable_thumbnail.png"
image_caption: |
  Mon MacBook Pro posé sur une table blanche, l'écran ouvert et montrant l'édition de ce billet sous VS Code.
---

_**Disclaimer**. Ceci n'est pas un publipostage. Je n'ai été contacté par aucune société citée dans ce billet ni pour l'écrire ni le faire relire. Il s'agit d'un billet à mon initiative propre et écrit en toute indépendance, qui relate mes réflexions au moment où j'ai souhaité changé d'ordinateur portable en me focalisant sur la réparabilité._

## Hommage au MacBook Pro mi-2012

Ah, mon MacBook Pro mi-2012. Un fidèle compagnon de route.

Il m'a bien servi pendant environ **10 ans**. C'est environ deux fois plus que la durée de vie moyenne d'un ordinateur portable [^0]. Je l'ai acheté en 2014 à quelqu'un qui l'avait gagné à une loterie (quel chanceux). C'était avec l'aide financière de quelqu'un qui se reconnaîtra et que je remercie. C'était donc du neuf… de seconde main.

[^0]: Source : [Répartition de l'obsolescence technologique des ordinateurs portables en France en 2019, par durée ](https://fr.statista.com/statistiques/1014056/distribution-obsolescence-technologique-ordinateurs-portables-france/), Statista.
Il m'a accompagné pendant toutes mes études en prépa puis en école d'ingénieur. À partir de 2018, j'y ai pratiqué la programmation de manière de plus en plus assidue, y compris sur des projets _open source_. À une époque, j'y ai même joué à des jeux vidéos ; en résolution plutôt faible pour les jeux un peu plus exigeants, mais sans jamais aucun problème pour les jeux indés (par exemple j'ai récemment redécouvert le [chef-d'oeuvre RCT2](https://www.youtube.com/watch?v=ESGHKtrlMzs) avec le formidable projet communautaire [OpenRCT2](https://openrct2.org/)).

Je m'y étais forcément un peu attaché. La preuve, je lui ai collé au fil du temps divers stickers, en bonne et due forme…

![Le capot du MacBook Pro. On y distingue, entre autres, les logos de Matrix, curl, DEV, Python, Hacktoberfest, du droit à la réparation, d'une association étudiante…](/static/img/mbp-capot.jpg)

Je tiens donc à lui rendre un certain hommage. D'autant qu'il est doté de certaines qualités que les modèles plus récents de la gamme d'Apple n'ont plus.

### Une réparabilité exceptionnelle (pour Apple)

Le MacBook Pro mi-2012 est en fait un ordinateur portable plutôt **réparable**. Il a un [score iFixit](https://fr.ifixit.com/laptop-repairability) honorable de 7/10. En comparaison, le score iFixit de la gamme a chuté à 1/10 dès le modèle de 2013, et il s'y est maintenu depuis. Le mi-2012 fait donc office **d'exception** dans la famille des MacBook Pro.

Voici d'ailleurs les améliorations que j'ai pu faire et qui ont contribué à sa longévité :

* En 2018, j'ai remplacé son disque dur (HDD SATA II) d'origine par un **SSD** (un Samsung 850 Evo). De quoi lui faire sacrément reprendre du poil de la bête. Le démarrage est passé de plusieurs minutes à une dizaine de secondes !
* Un peu avant cela, j'avais aussi augmenté sa **RAM** en remplaçant ses 2 x 2 Go = 4 Go de RAM DDR3 par 2 x 4 Go = 8 Go de RAM DDR3 (le maximum possible sur ce modèle) via 2 barettes Corsair d'occasion. Ça a globalement réduit les _lags_ liés à des applications gourmandes ou tournant à plusieurs en même temps. À ce jour il me semble que 8 Go de RAM est une quantité nécessaire et plutôt suffisante pour un usage de tous les jours.
* En 2021, j'ai remplacé la **batterie** d'origine qui avait atteint moins de la moitié de sa capacité d'usine, ne me laissant plus qu'environ 2h d'utilisation normale. Hélas, Apple ne fournissait plus de batteries compatibles. J'ai donc dû me rabattre sur une copie. Deux ans plus tard, la batterie est déjà très usée (60% de sa capacité d'usine).

### Obsolescence technologique, on y passera tous…

Ces 2 dernières années, les choses se sont néanmoins compliquées.

D'une part, le **processeur** [Intel i5 "Ivy Bridge" 3210M](https://ark.intel.com/content/www/us/en/ark/products/67355/intel-core-i53210m-processor-3m-cache-up-to-3-10-ghz-rpga.html) dont la conception date de 2011 semble atteindre ses limites. Ce n'est pas devenu un veau, mais j'ai très clairement remarqué un ralentissement. Un `brew update` prend très souvent _des plombes_ (certes, je ne le fais certainement pas assez souvent). Naviguer sur certains sites devient de plus en plus fastidieux, la faute revenant certes aux sites de plus en plus lourds, à rebours des tendances qu'il faudrait suivre (je vous regarde, Leboncoin, Facebook, et tant d'autres). Idem pour les logiciels de programmation comme VS Code, qui ne vont pas non plus en s'allégeant. Ah, la [loi de Wirth](https://fr.wikipedia.org/wiki/Loi_de_Wirth)…

D'autre part, ça y est, en 2023 le MacBook Pro mi-2012 est **définitivement obsolète** en ce qui concerne le **système d'exploitation macOS**. La dernière version majeure que j'ai pu y installer est macOS Catalina. Apple ne la supporte plus depuis septembre 2022. Je ne reçois donc plus de mises à jour de sécurité non plus. Ce modèle aura tout de même connu 8 versions majeures de macOS (de Mountain Lion sorti en 2012 à Catalina sorti en 2019 ; je l'avais pour ma part reçu avec Mavericks, sorti en 2014). Là aussi, côté OS, ce modèle a finalement été bien couvert… jusqu'à septembre 2022, donc.

Enfin, comme je l'ai indiqué plus haut, je ne pourrai plus me fournir en **batterie** qui durerait autant que celle d'origine. Il semble que je suis condamné à la remplacer tous les 1 ou 2 ans environ, jusqu'à ce qu'un accident arrive (il a été signalé des problèmes de gonflement sur l'un des seuls modèles compatibles que j'ai trouvé).

Tout cela me conduit à **anticiper le remplacement** de mon MacBook Pro avant que celui-ci ne me claque entre les doigts. Je pourrai ainsi garder le MBP en état opérationnel pendant la phase de transition. Une fois migré, je le revendrai, ou je l'enverrai à une société pour reconditionnement. Après tout, à part le fait qu'il soit obsolète et devienne trop lent pour mon utilisation, il fonctionne encore très bien.

## De macOS à Linux

Pour diverses raisons, je ne reprendrai pas un ordinateur portable Apple.

La première est liée au fait que je veux **un ordinateur réparable**. Or ceux qu'Apple fabrique aujourd'hui ne le sont pas du tout. Comme dit plus haut, leur score iFixit est d'un catastrophique 1/10 depuis le modèle de 2013. La [vue éclatée du MacBook Pro 2019](https://fr.ifixit.com/Tutoriel/Vue+%C3%A9clat%C3%A9e+du+MacBook+Pro+16-Inch+2019/128106) sur iFixit relate les divers problèmes : processeur, RAM et mémoire flash soudées sur la carte mère, colle et rivets rendant le démontage sans casse difficile, capteur Touch ID verrouillé sur la carte mère et qui sert aussi de bouton de marche…

La deuxième raison est que je suis définitivement bien plus attiré par **le monde libre et ouvert de Linux** que par le monde captif et fermé d'Apple. Je veux un ordinateur qui reste **un outil** que je peux maîtriser, bidouiller, réparer, améliorer. (Facile à dire pour un informaticien, vous me direz.) Or les machines Apple ne répondent bien sûr globalement pas à cette philosophie, à fortiori en ce qui concerne leurs iPhone. C'est aussi pour cette raison que je vais user mon iPhone 6s, puis que je me tournerai vers un autre appareil, comme un [Fairphone](https://www.fairphone.com/fr/) équipé de [/e/OS](https://e.foundation/e-os/).

La troisième raison est qu'Apple est une multionationale qui n'a pas (et ne peut probablement pas avoir) de considérations particulières en matière de droits humains, de traçabilité des composants ou d'impact environnemental. Si jamais il existe un fabricant de type Fairphone pour les ordinateurs portables, qui se construit dès le départ avec ces aspects en tête, ça sera un bon point.

Je n'ai, enfin, pas de raison ni d'envie particulière de retourner sous Windows.

La conclusion est donc toute trouvée : en ce qui concerne mon ordinateur personnel, je vais **quitter Apple**, et par conséquent macOS, pour **passer sous Linux**. Concrètement, [Ubuntu](https://www.ubuntu-fr.org/) ou une de ses variantes fera très probablement l'affaire.

## Anticiper la migration

Je souhaite bien sûr éviter le scénario catastrophe : que le MacBook Pro me claque entre les doigts et que, pour éviter de perdre toutes mes données, je sois obligé d'en retrouver un autre en urgence…

Pour cela, j'ai pensé qu'il valait mieux **anticiper**.

D'abord, bien sûr, les **fichiers**. La sauvegarde Time Machine, format propriétaire d'Apple, ne me sera évidemment d'aucune utilité. J'ai déjà procédé à la sauvegarde sur mon disque dur externe de mes données les plus importantes : dossier [Nextcloud](/fr/posts/2023/02/migration-dropbox-nextcloud), musique, photos, dossiers liés à la programmation (dont des archives que je n'ai pas forcément sous `git`), notes, et tous les autres documents importants.

Ensuite, les **logiciels "métier"**. Je veux parler des logiciels qu'on utilise au quotidien et sans lesquels on ne pourrait pas utiliser l'ordinateur pleinement.

### Des logiciels propriétaires aux logiciels libres : pas évident…

Concernant la **bureautique**, j'ai assez peu de besoins. Pour le Web et toutes les applications qui tournent désormais là-dessus, Firefox est très bien. Pout la bureautique à l'ancienne, j'utilise de toute façon déjà LibreOffice pour les quelques fois où j'ai besoin d'un tableur ou d'éditer un document. Si besoin, je peux toujours ouvrir un fichier via [OnlyOffice](https://personal.onlyoffice.com). Pour les fichiers textes simples destinés à moi-même, je préfère de toute façon le Markdown.

Par contre il y a un ensemble de logiciels que j'utilise et qui auraient pu être difficiles à migrer : les logiciels de musique assistée par ordinateur (MAO).

Sous macOS, Mainstage me permet, pour la modique somme de 30€ payés une bonne fois pour toute, d'avoir un ampli pour la guitare électrique, un synthéthiseur contrôlable par un clavier-maître MIDI, un processeur vocal, ou encore un mixeur pour tout cela. C'est très pratique et très "_It Just Works_".

Je savais que je n'allais pas retrouver une telle facilité d'utilisation sous Linux. Mais je ne pensais pas pour autant que tout un **écosystème de la MAO sous Linux** pouvait exister.

En effet, en me renseignant, je suis tombé assez vite sur le site [linuxmao.org](http://linuxmao.org). Une véritable mine d'or.

Idéalement, avant de faire la transition, mieux vaut expérimenter un peu. Ne dites rien aux collègues, mais j'avais la chance d'avoir une machine tournant sous Ubuntu à disposition : l'ordinateur du boulot… qui est chez moi puisque je pratique le télétravail. [En septembre 2022](https://twitter.com/florimondmanca/status/1569785355359887361), j'ai donc pu expérimenter un peu ce que donnait l'écosystème MAO de Linux.

C'est ainsi que j'ai découvert :

* [Ardour](https://ardour.org/), un <abbr title="Digital Audio Workstation">DAW</abbr> libre et _open source_ de bonne facture (il est à comparer à des logiciels comme Logic Pro X, Ableton ou encore Cubase). Je l'utilise pour les fonds sonores et synthéthiseurs d'un groupe amateur dans lequel je joue. J'y ai d'ailleurs souscrit pour soutenir le projet financièrement et obtenir les mises à jour [^1].
* [JACK](http://linuxmao.org/Jack), LE système de routage des flux audio entre applications sous Linux. Conformément à la [philosophie d'Unix](https://fr.wikipedia.org/wiki/Philosophie_d%27Unix), l'écosystème MAO sous Linux semble s'appuyer sur JACK pour faire collaborer les applications audio entre elles : la sortie de telle application va dans l'entrée de telle autre, et ainsi de suite jusqu'à la sortie système...
* [Guitarix](https://guitarix.org/), un simulateur d'ampli de guitare qui fonctionne avec JACK.
* [Surge XT](https://surge-synthesizer.github.io/), un synthétiseur _open source_, que je peux utiliser avec mon clavier-maître MIDI.

[^1]: Ardour est en effet un logiciel libre dans le sens où le code source l'est, mais le développeur fournit les versions compilées contre paiement ; un compromis plutôt sain pour la longévité du projet, non ?

Le seul hic, c'est que je n'ai pas encore réussi à faire fonctionner la chaîne complète sans qu'un horrible cliquetis finisse par apparaître quelque part entre la guitare et l'enregistrement dans Ardour. Pour régler ça, je devrai peut-être regarder du côté de [Ubuntu Studio](https://doc.ubuntu-fr.org/ubuntu_studio), une variante d'Ubuntu apparemment spécialisée dans le traitement audio en temps réel. Je fais en tout cas le pari que je finirai bien par trouver une solution, puisque de toute façon beaucoup de monde semble réussir à faire de la MAO en toute quiétude sous Linux.

## Quel matériel choisir ?

Alors très bien, je vais migrer sous Linux, et côté logiciels ça semble le faire. Mais quel matériel choisir pour remplacer le MacBook Pro mi-2012 ?

Mon fidèle MacBook m'a prouvé une chose, s'il fallait encore le prouver : un **ordinateur réparable**, ça permet effectivement de **faire durer le matériel dans le temps**. C'est aussi plus économique, et moins impactant d'un point de vue environnemental.

Alors voilà mon critère numéro 1 : un ordinateur portable sur lequel je pourrais **remplacer les composants principaux** en cas de défaillance ou d'un besoin d'évolution. Au minimum, la RAM et le stockage. Mieux : l'écran et le clavier, qui sont sujets à la casse et aux accidents. Encore mieux : la carte mère (pour passer à un processeur plus récent, par exemple).

Deuxième critère important, le **prix**. Je suis OK pour mettre le prix si la performance et la réparabilité y sont, puisque ça sera parti pour durer, mais ça doit rester raisonnable. Disons 1300 € maximum, soit le prix d'entrée actuel d'un MacBook Pro neuf.

### Les ordinateurs portables why!

Chez [Fairness](https://fairness.coop), dans un contexte professionnel, j'utilise déjà un ordinateur du fabricant suisse [why! computing](https://whyopencomputing.com). Il s'agit d'un why! NV41MZ pris en leasing chez [Commown](https://commown.coop). Equipé d'un Intel Core i7 de 11ème génération (l'Intel Core i5 de mon MBP était de 3ème génération...), de 16 Go de RAM et d'un SSD de 500 Go, il est tout-à-fait adapté à mon usage professionnel (bureautique classique et programmation informatique intensive). Je pense qu'il le serait tout autant à un usage perso. Je pourrais peut-être même m'en sortir avec 8 Go de RAM. (Hélas je ne pourrai pas réutiliser les barettes de RAM DDR3 de mon MacBook Pro, puisque les modèles why! semblent requérir des barettes DDR4, plus récentes ; idem pour le SSD SATA II de mon MacBook Pro, il faut obligatoirement un SSD compatible NVMe.)

Les ordinateurs portables de why! ont tous un excellent [indice de réparabilité](https://www.ecologie.gouv.fr/indice-reparabilite). Le score le moins élevé sur la [liste de leurs ordinateurs portables](https://whyopencomputing.com/fr/5-laptops-why) est de 9,4/10. Réparabilité : check. ✔ (En comparaison, mon MBP mi-2012 et sont 7/10 peuvent palir...)

Le [L140PU-i7 14"](https://whyopencomputing.com/fr/laptops-why/1336-178547-portable-why-l140pu-i7-14.html#/1-espace_de_stockage_2-aucun/51-memoire_ram-8_gb_1_x_8_gb/58-clavier-francais_azerty/100-systeme-ubuntu_2204_lts/142-espace_de_stockage_1-ssd_m2_500_gb_970_evo_nvme/253-garantie-2_ans/374-memoire_ram_2-8_gb_1_x_8_gb_3200_mhz), modèle qui m'intéresse le plus, est disponible dans une configuration qui me convient (16 Go RAM, 500 Go SSD) pour 1365 €. Prix : OK, check. ✔

### Le Framework Laptop

Durant mes recherches, je suis aussi tombé sur le [Framework Laptop](https://frame.work).

On peut dire que le marketing et la mise en forme sont plus alléchantes que pour why!. Pour preuve, Framework a été [discuté](https://news.ycombinator.com/item?id=28606962) [plusieurs](https://news.ycombinator.com/item?id=26263508) [fois](https://news.ycombinator.com/item?id=32179842) sur le site orange. Tout de même. Et en des termes plutôt élogieux, même si certains semblent déçus par des specs ou une réalisation un peu en deça de ce que peuvent produire les géants du laptop. Comme quoi, la _hype_ est à relativisier.

Le prix semble plus élevé que chez why!. Pour une configuration similaire (Intel Core i7, 16 Go RAM, 500 Go SSD, des connecteurs, livré sans OS pour y installer Linux), le prix s'élève à environ 1600 €.

### La réparabilité et ses subtilités...

Au global, le concept de why! et de Framework est très similaire : concevoir un ordinateur portable réparable qui puisse tenir la durée, en fournissant des guides de réparation pour les divers procédures ainsi que des pièces détachées.

Néanmoins, why! me semble être un poil mieux placé en ce qui concerne les subtilités de la réparabilité.

Sur le Framework, il y a 4 ports USB-C sur lesquels on peut (doit ?) brancher des "cartes d'extension", pour avoir par exemple un port HDMI, des ports USB-A, etc. Pourquoi ne pas avoir proposé un ensemble de ports sensé, voire seulement des ports USB-C qui auraient permis de se fournir en adaptateurs autres que ceux créés par Framework ? Je trouve que ça fait un peu gadget, voire que cela pourrait nuire à la durabilité (des pièces mobiles, ça s'use). Et peut-être même à la réparabilité, en plus de la raison qui suit…

Une autre différence non-négligeable a été signalée par le directeur de why! lui-même, François Marthaler, dans [l'épisode "Un ordinateur réparable" (71) de Techologie](https://techologie.net/episodes/71-ordinateur-reparable/). La question est la suivante : que se passe-t-il si le fabricant met la clé sous la porte ? Framework déclare avoir publié des plans en _open source_, et c'est tant mieux. Mais François Marthaler argue que les détenteurs d'un Framework pourraient tout de même avoir du mal à s'approvisionner en pièces détachées, car la société n'indique pas ses fournisseurs, lesquels vivraient sûreent plus longtemps qu'elle. À l'inverse, why! indique se fournir auprès de [Clevo](https://en.wikipedia.org/wiki/Clevo), un fabricant de _barebooks_ (ordinateurs portables nus destinés à la personnalisation) auprès duquel on pourrait donc obtenir des pièces détachées puisqu'on en connaît clairement la référence.

L'argument vaut ce qu'il vaut, vu la source dont il provient. Je le trouve néanmoins plutôt convaincant.

Au global, je penche pour l'instant pour le [L140PU](https://whyopencomputing.com/fr/laptops-why/1336-178522-portable-why-l140pu-i7-14.html). En tout cas, why! est un fabricant à envisager sérieusement, d'autant que j'ai un bon retour d'expérience suite à mon usage professionnel. (Cela dit, je dois avouer que la _hype_ autour du Framework et son marketing lêché jouent très clairement sur mes biais cognitifs ; en même temps qu'ils me rendent un peu sceptiques…)

## Maintenant, au boulot

Voilà pour ces quelques réflexions dont j'ai tenu à garder une trace écrite.

Je publierai peut-être un nouveau billet quand la migration aura été effectuée, avec un petit retour d'expérience sur la nouvelle machine et la MAO sous Linux. À plus !
