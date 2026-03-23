# Gestion du fork et des projets Django avec cruft

## Architecture des branches

```
upstream/main  ──●──────────●──────────●──────────▶  (cookiecutter/cookiecutter-django)
                 │           │           │
origin/main    ──●──────────●──────────●──────────▶  (miroir exact de upstream, ff-only)
                 │           │           │
custom         ──●──────────●──────────●──────────▶  (personnalisations jusana, rebasée sur main)
              [squash]    rebase       rebase
```

### Règles

- **`main`** : miroir exact de `upstream/main`. Jamais de commit personnel. Mise à jour par fast-forward uniquement (ou bouton "Sync fork" sur GitHub).
- **`custom_a_utiliser_pour_projets`** : toutes les personnalisations (htmx, solr, cookiebar, devcontainer, utils...). Rebasée sur `main` après chaque sync upstream.

---

## Créer un nouveau projet Django

```bash
cruft create --checkout custom_a_utiliser_pour_projets git@github.com:jusana/cookiecutter-django.git
```

Le fichier `.cruft.json` généré dans le projet contiendra le hash du commit de `custom` au moment de la création. C'est ce hash qui servira de référence pour les mises à jour futures.

---

## Mettre à jour le fork (sync upstream)

### Option 1 — Script automatisé

```bash
./sync-cookiecutter.sh
```

### Option 2 — Manuellement

```bash
# 1. Synchroniser main avec upstream
git checkout main
git fetch upstream
git merge --ff-only upstream/main
git push origin main

# 2. Tagger le tip actuel de custom AVANT le rebase (pour cruft — voir section dédiée)
git checkout custom_a_utiliser_pour_projets
git tag "cruft-base-$(date +%Y-%m-%d)"
git push origin "cruft-base-$(date +%Y-%m-%d)"

# 3. Rebaser custom sur le nouveau main
git rebase main
git push --force-with-lease origin custom_a_utiliser_pour_projets
```

> **Note :** Le bouton "Sync fork" de GitHub peut remplacer l'étape 1, mais les étapes 2 et 3 doivent toujours être faites manuellement en local.

### Conflits à anticiper lors du rebase

Ces fichiers sont modifiés régulièrement par upstream ET par les personnalisations :

| Fichier | Fréquence upstream |
|---|---|
| `requirements/base.txt` | quasi hebdomadaire |
| `requirements/local.txt` | très fréquent |
| `.pre-commit-config.yaml` | très fréquent |
| `config/settings/base.py` | occasionnel |

Les ~50 autres fichiers modifiés sont des ajouts purs (nouveaux fichiers) — jamais de conflit possible sur ceux-là.

---

## Mettre à jour un projet existant

Dans le repo du projet Django :

```bash
cruft update
# résoudre les éventuels conflits
git add . && git commit -m "chore: update from cookiecutter"
```

`cruft update` calcule le diff entre le hash stocké dans `.cruft.json` et le tip actuel de la branche `custom_a_utiliser_pour_projets`, puis applique ce patch sur le projet.

---

## Ajouter des personnalisations au template

```bash
git checkout custom_a_utiliser_pour_projets
# ... modifications ...
git add ... && git commit -m "feat: ma nouvelle perso"
git push origin custom_a_utiliser_pour_projets
```

Puis mettre à jour les projets existants avec `cruft update`.

---

## Vue d'ensemble sur la durée (exemple 3 projets)

```
upstream  ──A──────────B──────────C──────────▶
main      ──A──────────B──────────C──────────▶  (ff-only)
custom    ──[squash]──rebase─────rebase──────▶  (+commits perso)

projet1      ●──────────●──────────●            cruft update x2
projet2                 ●──────────●            cruft update x1
projet3                            ●            départ propre
```

---

## Compatibilité cruft et rebase

### Le problème

Cruft ne fait **pas** un `git diff` de commits — il régénère entièrement le template depuis le hash stocké dans `.cruft.json`, puis compare les fichiers générés. Pour cela, il doit pouvoir cloner le repo template **à ce commit précis**. Si ce commit a disparu du remote (force-push après rebase), `cruft update` échoue.

### La solution : un tag git avant chaque rebase

Avant le rebase, on crée un tag pointant vers le tip actuel de `custom_a_utiliser_pour_projets` et on le pousse. Après le force-push, le commit original n'est plus sur la branche mais reste **atteignable via le tag** — git ne GC jamais un commit référencé par un tag.

```
AVANT sync :
  custom  ──M3──C1──C2──C3           ← .cruft.json des projets → C3
                          │
                 tag "cruft-base-2026-03-22" (poussé sur remote)

APRÈS rebase sur M4 + force-push :
  custom  ──M4──C1'─C2'─C3'          ← nouveau HEAD
                 C3 n'est plus sur la branche MAIS reste accessible via le tag

cruft update dans un projet existant :
  clone template @ C3  ✅ (atteignable via tag)
  clone template @ C3' ✅ (HEAD de custom)
  diff fichiers(C3) → fichiers(C3') = patch upstream M3→M4 appliqué au projet ✅
```

Les tags `cruft-base-*` s'accumulent au rythme des syncs (quelques/an). Pour en supprimer un ancien :

```bash
git tag -d cruft-base-2026-01-15
git push origin :refs/tags/cruft-base-2026-01-15
```

> Ne supprimer un tag que si aucun projet actif n'a été généré entre ce tag et le suivant.
