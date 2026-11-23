# Model selection

Fill this in after you have trained your candidates in MLflow. Short sentences are fine. Use numbers from your runs.

## The question
What does this model decide, and who is hurt by a wrong answer? (One or two sentences.)

## Candidates
| Candidate | Why I tried it | AUC | F1 | F1 per slice (lowest) | p95 latency (ms) | Size (KB) | MLflow run ID |
|---|---|---|---|---|---|---|---|
| | | | | | | | |
| | | | | | | | |
| | | | | | | | |

## The champion
Which one did I pick, and what decided it? (Name the numbers that mattered and the ones I accepted losing.)

## My promotion rules
- Latency budget (p95): 30 ms, because logreg runs at about 7 ms and the forest at 33 ms on my laptop. CI runners are slower, so I kept a margin of about 3x for the models I want, while still excluding the slow forest.
- Minimum gain to replace the champion (F1 points): 0.01, because my test set is small and one split can move F1 by a point or more by chance. I don't want to redeploy for an improvement I can't trust.

## What I would check next
One thing that could make this choice wrong in production (for example a slice with few customers, or data that changes).
