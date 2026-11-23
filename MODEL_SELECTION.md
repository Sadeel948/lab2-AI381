# Model selection

## The question
The model predicts which customers will churn so retention can contact them. A missed churner (false negative) loses revenue; a false alarm (false positive) wastes a discount or a call.

## Candidates
| Candidate | Why I tried it | AUC | F1 | F1 per slice (lowest) | p95 latency (ms) | Size (KB) | MLflow run ID |
|---|---|---|---|---|---|---|---|
| logreg | Simple linear baseline: fast, tiny, easy to explain | 0.798 | 0.495 | 0.250 (one-year / two-year) | 7.1 | 4 | 42789fac7dff4403bdc4864a31f5cdb5 |
| random_forest | 200 trees, depth 8, to capture non-linear patterns | 0.759 | 0.454 | 0.222 (one-year) | 33.0 | 3160 | e8eed7b0a6f4413a849907480a18b1ff |
| gradient_boosting | 100 shallow trees, often strongest on tabular data | 0.748 | 0.417 | 0.222 (two-year) | 10.0 | 142 | 1f6ee2c9942041ff83530d16cfe89373 |

## The champion
I picked logreg. It has the best AUC (0.798) and F1 (0.495), the best F1 on month-to-month customers (0.543, the group that churns most), the lowest p95 latency (7.1 ms) and the smallest size (4 KB). Its weakest slice (0.25) is also the highest of the three. I accepted a weak one-year slice (0.25 vs 0.444 for gradient boosting) because that slice has few customers and its scores are noisy for every model. I also accepted that a linear model cannot learn feature interactions; on this data the more complex models did not benefit from that capacity.

## My promotion rules
- Latency budget (p95): 30 ms, because logreg runs at about 7 ms and the forest at 33 ms on my laptop. CI runners are slower, so I kept roughly 3x margin for the models I want, while still excluding the slow forest.
- Minimum gain to replace the champion (F1 points): 0.01, because my test set is small and one split can move F1 by a point or more by chance. I do not want to redeploy for an improvement I cannot trust. The cost is that a real but tiny improvement gets blocked.

## What I would check next
The one-year and two-year slices have few customers, so slice F1 can swing on a handful of people. I would count customers per slice and use cross-validation or a larger test set before trusting those differences. The gate also looks only at overall F1, so a candidate could win overall and still be worse on month-to-month customers; I would add a slice check to the gate.