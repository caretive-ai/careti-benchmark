# Careti Agent Benchmark

[English](README.en.md) | [한국어](README.ko.md) | [日本語](README.ja.md) | [中文](README.zh.md) | [Français](README.fr.md) | [Deutsch](README.de.md) | [Русский](README.ru.md)

---

**Système de benchmark mesurant les performances réelles des agents de codage IA**

## Résultats en direct

**[Voir les résultats du benchmark](https://careti.ai/fr/benchmark)**

## Pourquoi ce benchmark ?

### Limites des benchmarks existants

| Benchmark | Limite |
|-----------|--------|
| **HumanEval** | Mesure uniquement la génération de fonctions simples, déconnecté du développement réel |
| **SWE-bench** | Mesure la résolution de problèmes GitHub, mais ne reflète pas l'utilisation d'outils par l'agent |
| **MBPP** | Problèmes Python simples, pas de support pour les tâches multi-fichiers complexes |

**Problème central** : Les benchmarks existants ne mesurent que la "capacité de génération de code". Mais les vrais agents de codage IA (Cline, Cursor, Careti, etc.) **utilisent des outils, voient les erreurs et les corrigent, et font plusieurs tentatives**.

### Ce que ce benchmark mesure

```
Traditionnel : Problème → Modèle → Code → Note (1 fois)
Careti :       Problème → Agent → Code → Test → [Feedback d'erreur] → Nouvelle tentative → ... → Résultat final
```

## Derniers résultats (Hard Suite 100)

| Rang | Modèle | 1ère réussite | Réussite finale | Tentatives moy. | Coût |
|------|--------|---------------|-----------------|-----------------|------|
| #1 | Gemini 2.5 Flash | 62-67% | **98%** | 1.36-1.44 | $0.09-0.13 |
| #2 | GLM-4.7 | 89-92% | **97-98%** | 1.11-1.15 | $0.18 |
| #3 | Gemini 3 Pro (Preview) | 66-67% | **92-93%** | 1.53-1.57 | $0.60 |
| #4 | Solar Pro2 | 61-64% | **81-86%** | 1.82-1.87 | $0.75-0.87 |
| #5 | Solar Pro3 | 70% | **75%** | 1.71 | $1.35 |
| #6 | HyperCLOVA X | 1-2% | **1-2%** | 3.03-3.06 | $0.22-0.31 |

## Métriques clés

| Métrique | Signification | Pourquoi c'est important ? |
|----------|---------------|---------------------------|
| **Taux de réussite 1ère tentative** | Taux de succès au premier essai | "L'intuition" de l'agent - détermine le temps d'attente utilisateur |
| **Taux de réussite final** | Taux de succès incluant les nouvelles tentatives | "La capacité de résolution" de l'agent |
| **Tentatives moyennes** | Moyenne d'essais par problème | Indicateur d'efficacité |
| **Coût** | Coût total API | Faisabilité économique |

## Conditions de terminaison

| Condition | Description |
|-----------|-------------|
| `success` | Test réussi |
| `max_attempts` | Nombre max de tentatives atteint (5) |
| `timeout` | Délai dépassé (300s) |
| `oscillation` | Motif d'oscillation A↔B détecté |
| `same_error` | Même erreur répétée 3 fois |

## Données brutes

Le répertoire `results/` contient les données complètes du benchmark au format JSON.

### Structure des données

```json
{
  "problem_id": "he000-has_close_elements",
  "model": "Gemini 2.5 Flash",
  "success": true,
  "attempts": 1,
  "first_attempt_success": true,
  "total_time_ms": 5348,
  "cost_usd": 0.00018,
  "input_tokens": 161,
  "output_tokens": 264,
  "prompt_mode": "careti",
  "termination_reason": "success",
  "attempt_history": [...]
}
```

### Consultation des problèmes originaux

Les problèmes HumanEval peuvent être récupérés depuis le dataset Hugging Face :

```python
from datasets import load_dataset

ds = load_dataset("openai/openai_humaneval")
problem = ds["test"][0]  # he000 → problème 0
print(problem["prompt"])
```

**Hugging Face** : [openai/openai_humaneval](https://huggingface.co/datasets/openai/openai_humaneval)

## Licence

MIT

---

**Made by [Caretive](https://caretive.ai)** - Développeurs de l'agent de codage IA Careti
