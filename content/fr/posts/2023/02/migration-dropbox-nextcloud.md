---
title: |
  Au revoir Dropbox, bonjour Nextcloud
description: |
  Longtemps utilisateur de Dropbox, j'ai enfin migré mon stockage de fichiers personnels sur une solution libre. Je vous raconte pourquoi et comment ça s'est passé.
date: "2023-02-26"
category: retrospectives
tags:
  - til
  - logiciels-libres
image: "/static/img/articles/migration-dropbox-nextcloud.png"
image_caption: |
  Logo de Nextcloud.
---

Aujourd'hui, le **stockage de fichiers dans le _cloud_** fait partie d'une sorte de fondamental des outils numériques. Les solutions privatrices sont hégémoniques : Google Drive, iCloud, Microsoft OneDrive…

De mon côté, je stocke mes archives personnelles dans Dropbox depuis 2013 environ. Mais à l'heure où j'écris ces lignes, je viens de réussir la **migration vers Nextcloud**. Voyons ensemble comment ça s'est passé ! En bonus, je finirai par un court **guide de migration**.

## La petite histoire

J'utilise Dropbox depuis 2014 environ. J'y stocke d'abord quelques documents administratifs et supports de cours, mais mon usage s'intensif en 2015 quand je rentre en école d'ingénieur. Dropbox propose à ce moment-là une offre "_Student_" : mazette, 10 giga-octets de stockage gratos ! Je prends. Bien sûr, elle finira par expirer, me faisant revenir à la version gratuite de 2 Go, passée un peu plus tard à 3 Go.

À l'époque, Dropbox était presque exclusivement une solution de **synchronisation de fichiers dans le _cloud_**. Et ça fonctionnait _vraiment très bien_.

Mais **Dropbox était aussi une startup** : financée par de la _VC money_ [^0], elle ne pouvait pas se contenter de faire une seule chose et de la faire bien. Elle devait croître, s'ouvrir à de nouveaux marchés. Le retour sur investissement devait tomber.

[^0]: _VC_ signifie _Venture capitalist_, ou [capital risque (Wikipedia)](https://fr.wikipedia.org/wiki/Capital_risque) en français. Pour pouvoir se mettre au travail dans l'économie capitaliste, l'équipe de Dropbox réalise d'abord une levée de fonds auprès YCombinator en 2007, puis d'autres, et notamment en 2014 auprès de [BlackRock](https://www.youtube.com/watch?v=voSty1nfU-Q) (documentaire Arte, 2019). Source : [Dropbox - Histoire (Wikipédia)](https://fr.wikipedia.org/wiki/Dropbox#Histoire)

Dropbox s'est alors orienté vers le B2B (_Business to business_), et s'est désintéressé des particuliers, qui manifestement ne rapportaient pas d'argent. Ils ont lancé Dropbox Paper. Accueil mitigé [^1]. Ils ont mis à jour leur charte graphique. Le rendu était un peu curieux, mais admettons. Ils ont surtout considérablement augmenté le pallier d'entrée de l'offre "premium" : 200 € par an pour 1 000 Go. Clairement pas adapté pour mes besoins. Normal, je n'étais plus leur _cible_.

[^1]: Voir la discussion [Dropbox Paper](https://news.ycombinator.com/item?id=13523774), HackerNews, janvier 2017.

Bon, migrer vers autre chose, d'accord, mais quels étaient justement mes besoins ? Déformation professionnelle oblige, établissons un petit…

## Cahier des charges

En matière d'archivage numérique personnel, il me faut :

* 10 Go de stockage. C'est largement assez. J'ai environ 3 Go de fichiers sur Dropbox, et environ 2 Go de photos sur iCloud dont j'aimerais sortir ;
* Une **synchronisation** entre PC et mobile ;
* Une solution en **logiciel libre**, ou tout du moins open source, pour des raisons de sécurité des données et de meilleure portabilité ;
* Un hébergement en France, ou tout du moins en Europe, et si possible chez un hébergeur prenant garde aux **impacts environnementaux** côté _datacenter_ (PUE, utilsation de la ressource en eau, etc).

## Logiciels libres collaboratifs : nous y sommes

Il y a encore quelques années, la moindre accointance avec les logiciels libres collaboratifs risquait de donner des boutons.

Mais aujourd'hui, soit parce que les choses se sont vraiment améliorées, ou parce que j'ai pris le temps de vraiment les découvrir, **les logiciels libres collaboratifs semblent matures**. C'est enthousiasmant !

Quelques uns que j'utilise aujourd'hui régulièrement :

* [FramaSoft](https://framasoft.org) et ses divers outils en ligne. Par exemple, FramaForms remplace très bien Google Forms, et FramaPad rempalce Google Docs pour un usage basique ;
* [OnlyOffice](https://onlyoffice.com) pour les documents collaboratifs (quand FramaPad ne suffit pas) ;
* [Jitsi](https://meet.jit.si) pour la visio-conférence ;
* [Mattermost](https://mattermost.com) pour la messagerie instantannée. Mattermost a récemment ajouté le support multi-serveur au client mobile, une fonctionnalité qui freinait auparavant beaucoup l'adoption.

Ces outils libres (ou d'autres : BigBlueButton, RocketChat...) sont de plus en plus adoptés, y compris et notamment par les administrations publiques, ce dont je ne peux que me réjouir. Voir par exemple [apps.education.fr](https://apps.education.fr/), une liste d'outils proposées par le Ministère de l'Education Nationale, ou encore le [SILL](https://sill.etalab.gouv.fr/software) (Socle interministériel du logiciel libre) édité par Etalab.

## Bonjour, Nextcloud

Au vu de mon cahier des charges, [Nextcloud](https://nextcloud.com/) fait clairement le boulot.

Nextcloud est une suite logicielle collaborative. Elle propose notamment un stockage de fichiers de type Drive (Nextcloud Files). Il y a des clients PC (desktop) et mobiles pour la synchronisation. Et contrairement à Dropbox, Nextcloud est un logiciel libre. Son code source est ici : [github.com/nextcloud](https://github.com/nextcloud).

Il me restait la question de l'hébergement. Il n'y a pas d'instance Nextcloud principale, alors comment accéder à Nextcloud ? Est-ce que j'héberge ma propre instance (la flemme), et sinon, chez qui héberger mes données ?

## Il pleut des chatons

Nous avons la chance en France d'avoir une solution organisationnelle collective pour traiter la problématique de l'hébergement de solutions libres : [CHATONS](https://chatons.org). C'est un collectif de structures qui hébergent des solutions libres à destination de particuliers, professionnels, associations ou autres organisations.

J'ai pu voir la puissance de ce modèle chez [Fairness](https://fairness.coop) lorsque l'on a migré notre messagerie instantannée de Slack vers Mattermost. Moyennant une centaine d'euros par an, nous utilisons l'instance mutualisée de [Pâquerette](https://paquerette.eu), avec beaucoup de satisfaction jusqu'ici.

Après avoir consulté la [liste des CHATONS Nextcloud](https://www.chatons.org/search/by-service?service_type_target_id=All&field_alternatives_aux_services_target_id=All&field_software_target_id=271&field_is_shared_value=All&title=), j'ai donc choisi d'aller sur le Nextcloud de [Zaclys](https://zaclys.com). Cette société propose un [hébergement "Famille"](https://www.zaclys.com/quel-cloud-pour-mes-besoins/) abordable : 2 Go gratuits, ou 10 Go pour 10 € TTC par an.

(Hé oui, ce n'est pas forcément gratuit. Toutes libres qu'elles soient, l'hébergement de ces solutions a un certain coût qu'il faut se répartir. Heureusement, ce coût est faible, ce qui permet aux membres des CHATONS de proposer le cas échéant des tarifs abordables (certains pratiquent aussi le prix libre, comme l'association [Nebulae](https://wiki.nebulae.co/books/informations-administratives/page/le-prix-libre-conscient/)). Il faut néanmoins respirer un bon coup : au fond, il est raisonnable de payer un peu pour des outils numériques aussi fondamentaux. La gratuité monétaire des services comme Google Drive n'est qu'illusoire, ces services se rémunérant (grassement) sur la collecte et la revente de données personnelles.)

## Alors, ça donne quoi ?

À l'heure où j'écris ce billet, j'ai complètement migré mes fichiers sur le Nextcloud de Zaclys. Il ne me reste plus qu'à désactiver mes applications Dropbox.

L'interface de Nextcloud est toute aussi intuitive et fonctionnelle que celle de Dropbox. Je ne suis pas perdu ! Elle est même plus simple d'utilisation, puisqu'elle se concentre sur la gestion des fichiers. À l'inverse, l'interface web de Dropbox est aujourd'hui polluée par des fonctionnalités annexes qu'on ne peut pas désactiver, ainsi que par ces insupportables invitations à "Passer à un forfait supérieur".

![Capture d'écran de la page d'accueil de mon Nextcloud. Un dossier "Documents" de 2.6 giga-octets contient ce que j'avais auparavant dans Dropbox.](/static/img/nextcloud-home.png)

Point bonus : j'ai accès à d'autres applications comme un agenda, un outil de création de sondages, et même de quoi gérer des recettes de cuisine... Moi qui utilise encore iCloud pour mon calendrier et qui écrit mes recettes sur papier ne sachant où les stocker, voilà qui m'inspire d'autres migrations !

La migration m'a quand même pris mon après-midi. J'ai notamment eu du mal à comprendre comment Nextcloud gérait la synchronisation. Au début je ne savais pas qu'il existait un client officiel pour PC. J'ai perdu du temps à essayer de trouver une solution WebDAV alternative au Finder de macOS, qui est lent et peu robuste. Pour vous éviter ces étourderies, vais donc finir ce billet avec un petit guide de migration.

## Guide de migration

1. Préparez le dossier contenant l'ensemble des fichiers à migrer. Dans mon cas, le dossier `~/Dropbox` était déjà prêt. Je l'ai dupliqué dans un dossier `~/Nextcloud`.
2. Ouvrir un compte Nextcloud sur une instance.
3. Après vous être inscrit-e, connectez-vous, et prenez vos marques avec l'interface web (personnaliser le profil, prendre connaissance des documents d'aide au démarrage...).
4. [Installez les clients Nextcloud](https://nextcloud.com/install/) pour mobile et PC (j'insiste : ne perdez pas de temps avec WebDAV pour la synchronisation). Le client PC est très similaire au client PC de Dropbox : c'est un _daemon_ (programme d'arrière-plan) qui synchronise un dossier local avec les données stockées dans Nextcloud. On peut travailler dans le dossier et la synchronisation se fait en arrière-plan, sans blocage. C'est très appréciable.
5. Lancez alors le client PC, et connectez-vous. Il vous faudra le nom du serveur Nextcloud (`acloud6.zaclys.com` en ce qui me concerne). Pointez alors la synchronisation sur le dossier à synchroniser. C'est parti pour le téléversement ! (_l'upload_ en franglais)
6. Une fois la synchronisation terminée, connectez-vous sur le client mobile, et vérifiez que vos fichiers sont bien accessibles.

Félicitations ! Comme moi, vous utilisez maintenant Nextcloud comme _cloud_ personnel. :-)
