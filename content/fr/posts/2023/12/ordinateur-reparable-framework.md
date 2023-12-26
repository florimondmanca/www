---
title: |
  À la recherche d'un ordinateur portable réparable, épisode 2 : le Framework
description: |
  Les signes de faiblesse du MacBook Pro continuant de s'accentuer, j'ai fait le choix de me ré-équiper, et j'ai opté pour un Framework. Je reviens dans ce billet sur la réflexion sous-jacente : pourquoi pas why!, quelle configuration pour le Framework, quel Linux, prix, considérations environnementales...
date: "2023-12-25"
category: retrospectives
tags:
  - numerique-responsable
  - logiciels-libres
---

J'ai écrit dans un précédent billet ma [réflexion sur la recherche d'un ordinateur portable réparable](/fr/posts/2023/06/ordinateur-portable-reparable) qui pourrait remplacer mon vénérable MacBook Pro (MBP) mi-2012 en fin de vie après 10 ans de bons services.

## L'heure du choix

Entre temps, de **nouveaux symptômes** sont apparus sur le MBP.

Côté logiciel, **d'autres logiciels se sont mis à ne plus recevoir de mises à jour** sous macOS 10.12 (Catalina), la dernière version que ce MBP mi-2012 peut faire tourner. Parmi eux, le client de synchronisation Nextcloud[^00] ! Celui-ci ne fonctionne plus sous Catalina depuis la version 3.10.1. C'est assez problématique, et ce n'est pas un bug malgré [l'étonnement d'autres utilisateurs](https://help.nextcloud.com/t/macos-client-3-10-1-not-on-catalina/172975) : la [documentation officielle](https://docs.nextcloud.com/desktop/3.11/installing.html) indique bien que seul macOS 12 (Monterey) ou supérieur est supporté, c'est-à-dire un MacBook Pro 2015 ou plus récent. Me voilà donc coincé sur 3.10.0 sans même plus avoir accès à des correctifs.

[^00]: J'ai précédemment écrit sur ma [migration vers Nextcloud](/fr/posts/2023/02/migration-dropbox-nextcloud).

Côté matériel, la **prise d'alimentation** du MacBook Pro a continué à se dégrader, rendant la charge compliquée car nécessitant de garder l'ordinateur en position absolument statique (compliquée l'utilisation sur ses genoux, dans le lit… le portable se transforme presque en fixe).

Malgré tout, ne fois **reconditionné**, je pense que le MBP pourrait encore servir plusieurs années. Il faudrait remplacer la batterie (déjà remplacée il y a 2 ans par un modèle générique), remplacer le port d'alimentation, réinitialiser l'OS, et bien le nettoyer. Il reste utilisable grâce aux 8 Go de RAM et au SSD que j'avais installés vers 2016.

Mais comme je l'écrivais, je préfère **ne pas attendre qu'il lâche** pour en changer. Si j'ai déjà pu migrer l'essentiel de mes données soit sur Nextcloud soit en sauvegarde sur un disque dur, il me reste quelques données à migrer nécessitant le MacBook en état de marche. C'est notamment le cas de mes projets musicaux composés avec [Ardour](https://ardour.org), dont le format n'est malheureusement pas interopérable entre macOS et Linux. Il me faudra donc exporter les fichiers audio et MIDI depuis le Mac, importer sur le nouvel ordinateur Linux, et vérifier que tout fonctionne.

En ce jour de Noël de l'an 2023, j'ai donc craqué : j'ai commandé un nouvel ordinateur portable.

## Le choix final : un Framework 13

Dans le billet précédent, ma conclusion était d'hésiter entre le [why! L140PU](https://whyopencomputing.com/fr/laptops-why/1336-178522-portable-why-l140pu-i7-14.html) et un [Framework](https://frame.work). Sans plus de suspens, j'ai finalement choisi un **Framework 13**.

### _<span lang="en">Why not_ why!_?</span>_

Avant de détailler la configuration que j'ai choisie pour le Framework, voici d'abord les raisons qui m'ont finalement fait **écarter le why!**.

Il faut d'abord savoir que j'utilise à titre professionnel un [why! NVM41MZ i5 loué chez Commown](https://shop.commown.coop/shop/product/why-nv41mz-i5-eco-14-le-poids-plume-abordable-356?category=2). L'usage est de type bureautique et développement web et logiciel (PHP, JS/TS, Python). La configuration est largement suffisante pour cet usage : CPU Intel Core i5 11ème génération (plus précisément i5-1135G7U), RAM 16 <dfn><abbr title="gigaoctet">Go</abbr></dfn> et SSD 512 Go. J'en suis globalement très satisfait.

Les why! tirent notamment leur **réparabilité** du fait de se baser sur le matériel du fabricant taïwannais Clevo, et j'écrivais dans le précédent billet que c'était un point très convaincant. (À ce propos, j'ai découvert le fabricant et grossiste informatique allemand [Terra](https://www.terra-computer.fr/), plutôt orienté matériel bureautique professionnel, car une proche en apprentissage s'est faite équiper par sa Région d'un [Terra 1417](https://www.terra-shop.fr/ordinateurs-portables/182-terra-mobile-1417-fr1220725-4039407068128.html). En plus du prix très intéressant (500 € pour un PC portable taillé pour la bureautique et loin de faire "cheap"), ce modèle a aussi une excellente note de réparabilité (9,7 sur 10). Je ne peux que constater la corrélation avec cette même base Clevo. Les retours de professionnels IT ont l'air bons aussi[^0]. Les responsables achats de la Région semblent avoir fait un bon choix !)

[^0]: Voir [ce topic sur tech2tech.fr](https://forum.tech2tech.fr/topic/7114-choix-marque-portable-a-%C3%A9viter-ou-prendre/) ou [ce topic sur commentcamarche.fr](https://forums.commentcamarche.net/forum/affich-28982040-concernant-l-achat-d-un-ordi-pc-terra).

Alors pourquoi un Framework et pourquoi pas un why! ?

Si je suis honnête avec moi-même, c'est qu'à conception et prix relativement équivalents, **je _désirais_ le Framework davantage**. Hé oui, je ne vais pas post-rationnaliser, pour un équipement personnel qui m'accompagnera les 10 prochaines années (et j'espère plus), le marketing et le design ont compté… L'anecote d'une collègue rencontrant d'embêtants problèmes de compatibilité matériel/logiciel sur son why! 15" (problèmes à la mise en veille) a achevé de me décider, surtout quand je prévois un usage de création musicale et traitement audio temps réel.

## Configuration du Framework

Un Framework donc, mais _lequel_ et _qu'est-ce qu'on met dedans_ ?

Une **démarche de sobriété** implique de choisir du matériel répondant à ses **besoins**, sans superflu.

Ça implique de **définir ses besoins**. Je l'ai fait en creux dans le précédent billet : un ordinateur portable personnel pour **10 ans et plus**, qui soit **réparable** (indice de réparabilité très élevé) et fiable, compatible **Linux**, pour un usage bureautique, développement logiciel (je fais encore de l'open source de temps à autre), et — plus contraignant — <dfn><abbr title="Musique assistée par ordinateur">MAO</abbr></dfn>.

### Génération

Le Framework existe en plusieurs (je le dis comme ça) "générations" (Framework 11, 12, 13, 16) et "variantes" au sein d'une même génération (en fonction du processeur). À l'heure où j'écris, les générations 11 et 12 sont épuisées, la génération 13 est en vente, et la 16 est en précommande (ce qui, soit dit en passant, me pose question[^1]).

[^1]: J'ai l'intuition qu'avec ces "générations" le Framework va suivre [la même trajectoire que le Fairphone](https://grisebouille.net/encore-un-nouveau-fairphone/). À savoir : une contradiction possible entre les ambitions environnementales, [certes atteintes sur le plan de la réparabilité](https://fr.ifixit.com/News/87664/fairphone-5-keeping-it-10-10), et un modèle économique qui reste basé sur la vente d'appareils neufs de plus en plus puissants. D'une part, leur prix croissant limiterait leur diffusion. La génération 13 démarre ainsi à 979 € contre… 1579 € pour la génération 16 ! D'autre part, l'enchaînement des "générations" ne tirerait pas pleinement parti de l'évolutivité permise en théorie par la conception modulaire. Les "générations" seront-elles "rétrofittables" sur le matériel des anciennes ? La [page de présentation du Framework 16](https://frame.work/fr/fr/products/laptop16-diy-amd-7040) n'en fait pas publicité.

La [génération 16](https://frame.work/fr/fr/products/laptop16-diy-amd-7040) est présentée comme se différenciant par ses "cartes graphiques évolutives". Et de préciser : _"Le module graphique […] permet des applications de jeux et de créativité intenses"_. Certes je prévois un usage audio/MAO, mais pas de jouer à des jeux vidéos gourmands ni de faire de l'édition vidéo dernier cri.

Donc la génération 16, pas pour moi.

Regardons la génération 13…

### Choix du processeur

La carte mère, et notamment le **processeur** monté dessus, constitue le premier facteur différenciant de **prix** parmi les Framework 13.

Il y a quatre variantes de processeurs :

* Soit du AMD Ryzen série 7040 (prix de base 979 €) ;
* Soit du Intel Core 13ème génération (sortie en 2023, donc la plus récente) :
    * i5-1340P (prix de base 979 €) ;
    * i7-1360P (+390 €, soit 1369 €) ;
    * i7-1370P (+820 €, soit 1799 €); 

Je suis loin d'être expert en processeurs… C**omment comparer ?** J'ai découvert pendant mes recherches [le site UserBenchmark et sa section CPU](https://cpu.userbenchmark.com) qui permet de comparer des processeurs testés en conditions réelles.

Premier constat, **le prix semble indicatif de la puissance** : plus la variante du Framework est chère, mieux son CPU est noté sur ces benchmarks.

Deuxième constat, [rien que l'i5-1340P explose déjà en performance l'i5-3120M qui équipe mon MBP mi-2012](https://cpu.userbenchmark.com/Compare/Intel-Core-i5-1340P-vs-Intel-Core-i5-3210M/m2033578vs2719). En même temps, dix ans les séparent…

Pourtant, mon MBP mi-2012 avec son i5-3120M est encore largement utilisable : un peu lent pour du dev, mais d'un autre côté capable de faire tourner une session [Ardour](https://ardour.org) avec 5 ou 6 pistes d'instruments virtuels en simultané...

Alors je me suis dit que l'i5-1340P, de dernière génération, serait _très largement suffisant_ pour les années à venir (et quelque peu surdimensionné pour mon usage en l'état actuel des [obésiciels](https://fr.wikipedia.org/wiki/Bloatware)). Cette [discsussion Reddit](https://www.reddit.com/r/framework/comments/qlyvmu/looking_for_opinions_on_choosing_i5_vs_i7_model/) suggère par ailleurs que l'i7-1360P n'apporte un gain de performance que de l'ordre de 10%. Ce faible gain provient peut-être du _thermal throttling_[^2]. Le [comparatif sur UserBenchmark](https://cpu.userbenchmark.com/Compare/Intel-Core-i5-1340P-vs-Intel-Core-i7-1360P/m2033578vsm2032791) le confirme. Selon moi, ça ne justifie clairement pas les presque 400 euros supplémentaires.

[^2]: Un processeur fonctionnant à plein peut ne pas atteindre sa puissance théorique en raison de l'étranglement thermique (en anglais _thermal throttling_ ou _[dynamic frequency scaling](https://en.wikipedia.org/wiki/Dynamic_frequency_scaling)_), qui permet d'éviter la surchauffe notamment sur ordinateur portable où les capacités de refroidissement sont limitées. Cela consiste à réduire la fréquence de fonctionnement à la volée en cas d'élévation de température.

Ce sera donc le Framework 13, variante i5-1340P.

### Mémoire, stockage...

Pour le reste, le choix est déjà plus facile.

* Côté mémoire : je pars sur 16 Go de RAM DDR4. Actuellement le MBP est équipé de 8 Go DDR3 (2 x 4 Go). Hélas je ne peux pas les y réutiliser car le format est différent (DDR4 vs DDR3). Les 8 Go m'ont suffi jusqu'ici mais en plein usage MAO c'était parfois limite. Point positif, Framework propose de choisir des barrettes de RAM reconditionnées, ce qui semble récent.
* Côté stockage : 512 Go de stockage SSD, comme sur mon MBP. Cette taille m'a été amplement suffisante, mais 256 Go aurait été trop peu. Là aussi, je ne peux pas réutiliser le Samsung 970 EVO que j'avais monté sur le Mac vers 2016 car l'interface n'est pas la même : SATA II pour le Mac (format disque dur) versus NVMe (plus compact) pour le Framework.

Je laisserai donc la RAM et le SSD équipant le MBP en place, ce qui sera de toute façon plus intéressant pour le reconditionnement.

### Système d'exploitation

Framework propose soit de fournir Windows, soit — quelle joie ! — de ne rien fournir pour qu'on puisse installer ce qu'on veut. Sous-entendu : un **Linux** !

C'est donc cette option que je choisis. Mon espoir est aussi que, comparé à macOS, _n'importe quel Linux_ permette de **limiter les effets d'obésiciels**, c'est-à-dire des effets de ralentissement du fait de l'alourdissement des logiciels.

#### La parenthèse Linux

Mais alors se pose cette question : **_quel Linux_** ? ([xkcd de circonstance](https://www.explainxkcd.com/wiki/index.php/456:_Cautionary).) Dans le billet précédent, la question était restée en suspens, notamment au vu de mes besoins MAO.

Là aussi mon expérience est très limitée. Au travail j'utilise tout simplement **Ubuntu**, qui me satisfait dans ce contexte et que je n'aurais aucun problème à recommander pour le grand public voulant passer à Linux pour de la bureautique et du Web. Mais j'avais rencontré des problèmes de décrochage lors d'un essai rapide avec [Guitarix](https://guitarix.org).

J'évoquais dans le billet précédent **[Ubuntu Studio](https://ubuntustudio.org/)**, une distribution intéressante car elle installe d'office de nombreux logiciels de création (on pourrait dire "trop"), mais surtout avec un noyau Linux "faible latence".

En alternative à Ubuntu, des collègues et amateurices de Linux m'ont aussi recommandé **[Linux Mint](https://www.linuxmint.com/)**. Cette distribution qui se veut "_<span lang="en">friendly</span>_" semble effectivement recevoir [bien des éloges](https://www.reddit.com/r/linuxmint/comments/o8bt2j/linux_mint_or_ubuntu/) ("_<span lang="en">Ubuntu done right</span>_", ça envoie).

Des recherches sur l'utilisation de Linux Mint pour de la MAO ont été fructueuses : des discussions Reddit ([une première](https://www.reddit.com/r/linuxmint/comments/pajjgu/setting_up_linux_mint_for_audio_production/), [une deuxième](https://www.reddit.com/r/linuxaudio/comments/mfuktq/comment/gsqz8g0/)) suggèrent que **Linux Mint pourrait aussi fonctionner pour de la MAO** ! Au mieux _<span lang="en">out of the box</span>_ — à tester. Au pire en installant `linux-lowlatency`, qui semble installer un noyau faible latence comme pour Ubuntu Studio (_je n'ai pas vraiment idée de ce que ça veut dire à ce stade_), et `ubuntu-studio-installer`, qui (sans le lancer) configurerait déjà JACK (le logiciel de routage audio pour Linux) et des "privilèges temps réel".

Point d'interrogation en revanche, Linux Mint n'est pas mentionné sur [la page distributions de linuxmao.org](http://linuxmao.org/Distributions), contrairement à Ubuntu Studio, mais aussi [KXStudio](https://kx.studio/) ou encore [AVLinux](http://www.bandshed.net/avlinux/). Or linuxmao.org m'est apparue être une référence francophone sur le sujet...

Bon, à creuser, mais si j'ai le Mac encore à disposition, je pourrai tester plusieurs distributions ! En commençant par Linux Mint, je pense.

### Cartes d'extension et autres options

Framework a un système de "cartes d'extension" — des modules d'interfaçage entre USB-C et d'autres interfaces (USB-A, HDMI, Ethernet...). Dans mon précédent billet j'écrivais que je trouvais ça assez gadget, mais finalement je ne trouve pas d'argument décisif contre. La possibilité de choisir ses interfaces en fonction de ses besoins est quand même intéressante.

J'ai choisi un module USB-C (obligatoire pour le chargement), deux modules USB-A (de nombreux appareils restent fournis avec des câbles USB-A, surtout dans la musique), et un module HDMI pour brancher un écran externe (moniteur, télévision, autre). À mon avis je n'aurai besoin de rien d'autre avant longtemps, puisque sur mon MBP je n'ai jamais utilisé les autres interfaces proposées (Ethernet, DisplayPort, MicroSD).

Quelques autres options sont proposées par Framework, comme la couleur du cadran d'écran, la fourniture d'un adaptateur secteur, la disposition du clavier... Je passe là-dessus, j'ai pris du classique. (Peut-être Framework proposeront-ils à l'avenir des adaptateurs secteur USB-C reconditionnés, comme ils le font pour la RAM ? Et comme ils pourraient aussi le faire pour le SSD…)

## Alors, combien ça coûte ?

On résume : Framework 13 en variante i5-1340P (la moins onéreuse), avec 1 x 16 Go DDR4 de RAM reconditionnée, un SSD de 512 Go, 4 "cartes d'extension", un adaptateur secteur.

Le tout pour : **1178 € TTC**.

Franchement, si les promesses qualitatives sont tenues, **je trouve ce prix très honnête**.

Il faut comparer par exemple au Dell XPS 13, référence en matière d'ultraportable haut de gamme. Il est vendu à 2500 € en configuration similaire mais avec un CPU moins puissant ([comparaison UserBenchmark](https://cpu.userbenchmark.com/Compare/Intel-Core-i5-1340P-vs-Intel-Core-i7-10510U/m2033578vsm891469)). Il est aussi moins réparable ([indice iFixit de 7 sur 10](https://fr.ifixit.com/Device/Dell_XPS_13), ce qui reste honnête).

S'il faut absolument comparer aux **machines Apple**, un MacBook Pro dernier cri est affiché à 2000 €, et 1650 € pour le MacBook Air M2. Les ordinateurs Apple sont donc **plus onéreux**. Certes, [leur performance semble un cran au-dessus](https://nanoreview.net/en/laptop-compare/framework-laptop-vs-apple-macbook-pro-14-2023) du Framework. On pourrait aussi évoquer l'ergonomie exemplaire des machines Apple (en version sans touchbar) que je ne nierais pas. Mais **côté réparabilité, ça n'a rien à voir**. iFixit n'a pas encore publié d'analyse de ces derniers modèles, mais ceux de 2019 avaient un [score de réparabilité iFixit](https://fr.ifixit.com/reparabilite/indices-ordinateur-portable) désastreux entre 1 et 3 sur 10 (inférieur d'ailleurs à l'indice de réparabilité français que la marque affichait[^3]).

[^3]: Hé oui, si l'on regarde l'indice de réparabilité français auto-déclaré par Apple, qui se retrouve affiché sur les étiquettes des distributeurs, on était plutôt à l'époque autour de 4 ou 5, et non 1 à 3 ! Aujourd'hui, les derniers modèles s'affichent autour de 6,5 sur 10. Où est l'arnaque ? iFixit l'a analysé en 2021 dans [un article dédié aux calculs de réparabilité d'Apple](https://fr.ifixit.com/News/69724/comment-apple-a-pu-calculer-ses-indices-de-reparabilite-francais). En clair, [les méthodologies d'iFixit et de l'indice français diffèrent](https://fr.ifixit.com/News/68847/pourquoi-lindice-ifixit-differe-de-lindice-de-reparabilite-francais) : sans surprise, l'indice français, passé par le filtre du processus législatif, est hélas plus laxiste. Sa conception permet à Apple d'obtenir de bons scores malgré de grosses lacunes. L'association Halte à l'Obsolescence Programmée (HOP) l'avait aussi fait remarquer en 2022 dans [un article se demandant si l'indice de réparabilité tenait ses promesses](https://www.halteobsolescence.org/lindice-de-reparabilite-tient-il-ses-promesses/) : il n'y a pas de mécanismes de seuils, il est donc possible d'avoir un zéro pointé sur un critère important, comme la démontabilité, et pourtant obtenir un bon score global. À l'inverse, être exemplaire sur les critères essentiels mais ne pas pouvoir tenir des critères secondaires, comme la capacité à livrer des pièces détachées rapidement (3 jours pour obtenir un 10 sur 10 au critère "Délai de livraison des pièces"), peut plomber votre score. C'est le cas du Fairphone 3 qui a [un indice de réparabilité français de seulement 8,7 sur 10](https://www.indicereparabilite.fr/produit/smartphone-fairphone-fp3/), ce qui ne reflète pas la réalité (il a [un score iFixit de 10 sur 10](https://fr.ifixit.com/Device/Fairphone_3) !).

Si on chérit la **réparabilité** et qu'on accepte de se passer d'une puissance superflue (en faisant des **économies** au passage), selon moi **le Framework bat la concurrence à plat de coûture**.

Il reste qu'à ce prix, on ne peut pas non plus dire que le Framework soit un équipement accessible à tout public. On reste sur du haut de gamme, _plutôt élitiste_. (Mais en apparence, je dirais ! Car 1200 € pour les 10 années et plus à venir, comparé à 500 € d'ordinateurs basse-moyenne gamme irréparables tous les 3 ou 4 ans, on s'y retrouve !)

Ne serait-il pas intéressant de proposer un modèle tout aussi réparable et bien conçu, mais moins puissant en se limitant à un usage plus bureautique, qui le rendrait donc _a priori_ moins cher ?

Hélas, comme je l'écrivais en bas de page [^1], Framework ne semble pas se diriger sur ce segment, certes extrêmement concurrentiel... Qui pourrait peut-être aussi être déjà bien couvert par why!, Terra, et autres fabricants basés sur Clevo. Passons le mot à nos proches, en leur faisant aussi des recommendations de machines d'occasion, reconditionnées ou (au pire) neuves avec les meilleurs [scores iFixit](https://fr.ifixit.com/reparabilite/indices-ordinateur-portable).

## Et niveau environnemental ?

J'ai rentré les caractéristiques les plus proches de ce Framework, de l'usage que j'en aurai et de la durée de vie que j'en attends dans [Datavizta](https://dataviz.boavizta.org).

Les résultats du simulateur indiquent 488 kg de CO2-équivalent sur tout son cycle de vie, dont 181 à la fabrication. (Je m'avoue encore peu en capacité d'interpréter les indicateurs autres que les émissions de <dfn><abbr title="Gaz à effet de serre">GES</abbr></dfn>.)

Sur 10 ans, cela représente [deux pavés de bœuf par an](https://ourworldindata.org/grapher/food-emissions-supply-chain). Honnête. (Enfin, ça rappelle surtout qu'il faut réduire sa consommation de viande.)

Ou encore 0.13 kg de CO2-équivalent par jour, soit 2 à 3% du budget "soutenable" d'environ 5 kg de CO2-équivalent que j'avais estimé dans mon [billet sur les vacances à vélo](/fr/posts/2021/09/vacances-velo#bas-carbone-verifions). C'est un peu moins que la place du numérique dans les émissions mondiales aujourd'hui (entre 3 et 4 %), donc ça semble cohérent.

C'est à comparer aux émissions de la fabrication d'un MacBook Pro 2020, que d'après les [données Boavizta](https://github.com/Boavizta/environmental-footprint-data/blob/main/boavizta-data-fr.csv) est de l'ordre de 200 à 250 kg CO2-équivalent en cycle de vie. Etalés sur 10 ans, ils seraient aussi "dans les clous" d'un budget bas carbone. Il faudrait peser les autres critères, bien sûr…

Tout ceci nous rappelle surtout que l'essentiel en matière d'équipement informatique est bien de **faire durer**.

## Et après ?

À l'heure où j'écris ce billet, le Framework est donc commandé et devrait arriver chez moi bientôt.

J'espère vraiment qu'il durera encore plus que le MacBook Pro, à savoir tenir et répondre à mes besoins pendant **10 ans et plus**. Je dirais que c'est vraiment, au doigt mouillé, le seuil minimum de durabilité d'un ordinateur portable. Je suis bien d'accord avec François Marthaler, fondateur de why!, qui considérait dans son [entretien Techologie](https://techologie.net/episodes/71-ordinateur-reparable/) qu'on devait pouvoir tenir un ordinateur "10, 15, 20 ans, et même plus !".

**Prochaine étape : la migration sous Linux**. J'ai _très hâte_ de finir ma sortie de l'écosystème propriétaire d'Apple, après être passé sous Fairphone + /e/OS il y a quelques mois <small>(comment, je n'ai rien écrit à ce sujet ici ?? On corrigera peut-être ça…)</small>.

En conclusion philosophique, non je ne pense pas que les logiciels et systèmes d'exploitation libres _suffiront_ à faire advenir un [numérique acceptable](https://louisderrac.com/alternumerisme-radical/#h-manifeste-pour-un-alternumerisme-radical-v1). Mais ils y contribuent très probablement. En tout cas, quel plaisir de reprendre la main sur son matériel ! Et à titre personnel, en tant que professionnel de l'informatique, je me dis que se mettre en cohérence, faire vivre l'alternative et en parler autour de soi, c'est la moindre des choses.
