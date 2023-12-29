## Déballage du Framework

Beau packaging...

Montage en 5 à 10 min

Les clips magnétiques sont ingénieux

## Installation de Linux Mint

Je suis le guide communautaire : https://guides.frame.work/Guide/Linux+Mint+21.2+Installation+on+the+Framework+Laptop+13/159

### Téléchargement de Linux Mint

Ici https://linuxmint.com/edition.php?id=305

Vérification des checksums : https://linuxmint-installation-guide.readthedocs.io/en/latest/verify.html

### Création de l'USB bootable

Logiciel : le guide communautaire ne mentione que Rufus qui est uniquement pour Windows (.exe)

Pour macOS, [la doc Linux Mint recommande Etcher](https://linuxmint-installation-guide.readthedocs.io/en/latest/burn.html#in-windows-mac-os-or-other-linux-distributions), qui fonctionne aussi bien sous Windows, Linux que macOS.

Petit problème, le bouton "Flash from File" se désactive quand on clique dessus et la boîte de dialogue de sélection de fichier ne s'ouvre pas. Probablement un problème de permissions (le système de permissions a été drastiquement contraint à partir de macOS Catalina).

Direction Paramètres > Sécurité et confidentialité > Confidentialité > Accès complet au disque > Ajouter, en choisissant l'application `balenaEtcher`.

Voilà, on peut sélectionner le `.iso`.

### Installation

Seul problème rencontré par rapport au guide :

Après avoir redémarré, l'écran affiche une liste infinie d'erreurs de type `SQUASHFS error: unable to read data [...]`.

Une recherche en ligne a suggéré que cela pouvait signifier que l'écriture du ISO sur la clé USB d'installation contenait une erreur. Pourtant j'ai pu installer Mint !

Heureusement, il a suffi que j'éteigne l'ordinateur (appuyer longtemps sur le bouton de démarrage) et que je débranche la clé USB. En démarrant, c'est bon, j'arrivais sur Linux Mint. Je suppose qu'en laissant la clé USB branchée, l'ordinateur essayait de booter à nouveau dessus ce qui pour une raison que j'ignore ne fonctionne plus après l'installation.

Ensuite je suis le guide de finalisation https://github.com/FrameworkComputer/linux-docs/blob/main/LinuxMint21-1-Manual-Setup-13thGen.md

## Configuration des sauvegardes

Cette personne fournit le très bon conseil de configurer les sauvegardes dès que possible, et d'en faire une à chaque étape importante de l'installation, à commencer par juste après l'installation

https://community.frame.work/t/responded-new-user-already-floundering/29149/36

Je suis ce guide pour faire ma première sauvegarde : https://itsfoss.com/backup-restore-linux-timeshift/

Depuis le Mac, je crée avec l'utilitaire de disque une partition dédiée sur le HDD que j'utilisais pour la sauvegarde du Mac.

J'avais 4 partitions : Stockage 1, Stockage 2, Free, Sauvegarde Mac. Stockage 1 contient l'essentiel de mes fichiers, il me restait à y déplacer les Films stockés sur Stockage 2. J'ai pu ensuite retirer Stockage 2 et Free puis recréer une partition de 256 Go en FAT32. La partition Sauvegarde Mac s'en est retrouvée agrandie. Je l'effacerai depuis le Framework quand j'aurai entièrement terminé la migration.

Malgré tout, une fois le HDD branché au Framework, Timeshift indique "Le périphérique sélectionné n'a pas de partition Linux".

Le guide suggère qu'une "partition Linux" signifie une partition au format Ext4. J'ouvre donc l'application "Disques" de Mint pour formatter la partition au format Ext4. Après rafraîchissement, cette partition est sélectionnable dans Timeshift !

J'ai créé ma première sauvegarde, avec un commentaire : "Post-installation et réglages basiques"

Puis j'ai créé un dossier "test" sur le bureau, et j'ai restauré l'ordinateur à partir de cette première sauvegarde. Le dossier n'est plus là : tout va bien la restauration de sauvegarde fonctionne !

## Installation des logiciels

Firefox est installé par défaut, chouette.

Pour me connecter à mon compte, il me faut mes mots de passe.

En avant pour installer KeePass ! Avec le paquet `keepassx`, qui pèse d'ailleurs seulement 490 ko. Je transfert mon fichier de mots de passe du Mac au Framework par clé USB, je charge dans KeePass, et hop ! J'ai accès à mes tous mes mots de passe sur le Framework. Je vais pouvoir me connecter aux différents services.

* KeePassXC
* Client de synchronisation Nextcloud
* Telegram Desktop
* VSCodium
* Discord
* Mattermost

Configuration Thunderbird

* Calendriers Nextcloud : via CalDAV avec l'extension TBSync pour Thunderbird
* Emails : via ProtonMail Bridge

Et hop, sauvegarde !

## Migration des données issues du MBP

J'avais sauvegardé mes données importantes sur le disque dur externe. Je les recopie donc sur le Framework.

J'en profite aussi pour importer les fichiers Nextcloud qui n'avaient pas été synchronisés par défaut car trop volumineux : mon dossier principal et mes photos.

Puis hop, sauvegarde !

## Rangement des données migrées

Une fois les données recopiées, je fais un peu de rangement.

Notamment, je nettoie ma bibliothèque musicale et je configure au passage Rhythmbox qui a l'air d'être un remplaçant satisfaisant d'iTunes / Apple Music.

Et hop, sauvegarde !

## Outils de développement

En avant pour la configuration des outils de dev...

* Git n'était pas installé : `sudo apt install git`
* Configuration SSH pour Git : création d'une clé SSH, enregistrement dans GitHub, activation des [commits signés]
* Installation de [zsh] et [ohmyzsh] ainsi que [Starship]
* Installation de Python indépendante de la version système avec [pyenv]
* Installation de Node.js avec [nvm]
* Configuration de VSCodium, pour pouvoir y utiliser zsh, notamment...

Ensuite je configure mon accès SSH à la VM où tourne le présent blog pour pouvoir y déployer.

Mine de rien tout ceci m'a pris deux bonnes heures, le temps de trouver sur le Web des réponses aux divers petits problèmes qui apparaissaient...

Et hop, sauvegarde !

## Ardour, etc

Pour la MAO sous Linux, j'utilise [Ardour](https://ardour.org). J'ai en particulier une session Ardour utilisée pour un tribute band qui contient tous les backing tracks des morceaux qui en nécessitent, avec pistes audio et pistes de synthétiseurs réalisées essentiellement avec l'excellent synthétiseur libre [Surge XT](https://surge-synthesizer.github.io/).

Lorsque nous avons commencé à avoir besoin de ces backing tracks, j'ai mis tout le dossier de la session Ardour dans git et je l'ai poussée vers un hébergeur, d'abord GitHub puis [Codeberg](https://codeberg.org).

Le pari était que _plus tard, quand je serai sous Linux_, je pourrais réimporter telle-quelle la session développée sous macOS.

Est-ce que le pari est tenu sous Linux Mint ? Magnifiquement, la réponse semble être oui !

(D'abord, une petite sauvegarde pré-configuration d'Ardour. Hop !)

J'ai installé Ardour avec l'installateur Linux tout fait que l'on peut télécharger après abonnement [^0].

[^0]: Ardour a un modèle de logiciel essentiellement libre mais dont les binaires compilés ne sont accessibles qu'après [abonnement mensuel](https://community.ardour.org/subscribe) à un montant de 10 dollars par mois, ceci afin de soutenir le développement (on peut toujours compiler Ardour librement). Cela me semble sain vu la criticité d'un tel logiciel pour la communauté. J'aurais cependant préféré un montant libre avec un plancher par exemple. Cela dit l'abonnement n'a d'intérêt que pour recevoir les mises à jour. Il est possible de payer $10 une fois puis de se désabonner et de garder la version téléchargée à ce moment là pour toujours. J'ai néanmoins pu constater qu'Ardour s'améliorait encore substantiellement de version en version.

À l'ouverture de la session, pas d'obstacle majeur : la session s'ouvre ! Lors d'un test précédent sous Ubuntu, la session éditée sous macOS ne s'ouvrait même pas. J'en suis très heureux car cela va m'éviter une migration fastidieuse à base d'exports MIDI et de reconstitution des pistes et des automatisations.

Petit contretemps cependant, Surge XT n'est pas reconnu. Il semble que l'installation de Surge XT par le Software Center ne fonctionne pas bien, je ne vois même pas la GUI s'afficher quand je le lance indépendamment. Je passe par le [paquet Debian téléchargeable](https://github.com/surge-synthesizer/releases-xt/releases), et là c'est bon.

Deuxième contretemps, dans la configuration Audio/MIDI, avec le "système audio" configuré sur "ALSA", je n'ai pas de son, même en reconfigurant correctement le routage audio interne à Ardour. La "sortie système" n'émet pas de son vers mon casque.

Suite à ce problème, j'ai fait un détour par JACK duquel je ne suis sorti qu'en revenant à ALSA, ce dernier étant le système son "par défaut" (enfin, ça a l'air compliqué) sous Linux Mint...

En effet [ALSA ne parle pas le Bluetooth](https://discourse.ardour.org/t/bluetooth/89529/3). Après avoir branché mon casque en filaire : c'est bon, j'avais du son dans Ardour !

Il se peut que sans rien faire d'autre tout ait pu fonctionner, mais il se trouve que j'ai aussi installé JACK entre temps pour voir si Ardour fonctionnerait avec celui-ci. À tout hasard, voici comment. Je l'ai installé via [Ubuntu Studio Installer](https://ubuntustudio.org/ubuntu-studio-installer/) avec `sudo apt install ubuntustudio-installer`. En faisant utiliser JACK à Ardour avec le backend ALSA, j'avais une erreur "Cannot use real-time scheduling (1: Operation not permitted)" en provenance de JACK, que je pouvais reproduire avec `jackd -dalsa -dhw:0`. Au final je suis donc repassé sous ALSA avec casque filaire.

Côté carte son, la Focusrite 2i2 est détectée directement par le Framework une fois branchée. Je règle Ardour pour qu'il y envoie la sortie son, et hop j'ai du son en branchant mon casque filaire sur les sorties de la Focusrite. J'ai quand même dû reconfigurer les "Audio Connections" car initialement Ardour n'avait rien branché sur la sortie système. À gauche j'envoie le mix Click track + Backing track pour le batteur. À droite, le Backing track uniquement qu'on enverra dans la sono via la table de mixage 

Prochaine étape, l'installation d'[Open Stage Control] (OSC), qui permet de contrôler le playback d'Ardour via une interface simplifiée en gros boutons, pratique pour le live. De ce côté-là aucun soucis, après configuration, OSC réussit à contrôler Ardour.

Ensuite : le MIDI. Actuellement, mon pédalier voix reçoit des signaux MIDI pour déclencher automatiquement des harmonies. Après avoir branché le pédalier et configuré la sortie MIDI dans Ardour, aucun problème, les signaux MIDI sortent.

Bien. Dernière étape : le VST3 que j'ai utilisé pour les cordes sur un morceau.

Celui que j'utilisais est [LABS Strings](https://labs.spitfireaudio.com/strings), un VST3 propriétaire. Il est uniquement compatible avec Windows ou macOS. En plus de ça, il faut installer une application séparée pour pouvoir _ensuite_ installer le VST3. Compliqué.

Je change alors pour [OT Strings](https://musictop69.wixsite.com/orchestools/orchestools-two), un VST3 compatible Linux, qui est aussi libre (GPLv3) ! Voilà qui va m'éviter de devoir bidouiller avec [yabridge](https://github.com/robbert-vdh/yabridge) pour faire tourner du VST3 Windows sous Linux avec Wine.
