# OCD Patient Strategic Insights

## Executive Summary

This project segments OCD patients by clinical severity, age, and family-history
signals to support more targeted care operations. The analytical workflow turns
raw patient records into validated features, interpretable clusters, statistical
evidence, and reusable figures. The core business value is better triage:
identify high-risk cohorts earlier and allocate clinical follow-up capacity
where it can create the greatest patient impact.

## Strategic Insights

1. Prioritize the highest-severity cluster for proactive outreach. The cluster
   with the highest average Y-BOCS score should be the first candidate for
   enhanced follow-up, appointment reminders, and care-plan review.
2. Treat the Extreme severity rate as a capacity-planning metric. A rising
   share of Extreme cases indicates higher clinician workload, longer visit
   complexity, and stronger need for escalation pathways.
3. Use family-history concentration as an early-screening signal. Segments with
   high family-history rates are candidates for education, preventive screening,
   and earlier intervention.
4. Use symptom association rules to improve intake workflows. Strong
   obsession-compulsion links can inform checklist design and help clinicians
   probe for likely co-occurring symptoms.
5. Pair statistical significance with operational significance. ANOVA results
   should be reported with p-values and group means, then translated into a
   decision such as whether a group warrants targeted support.

## Key Metrics Presentation Guide

- Retention Rate: For longitudinal care data, define retention as patients with
  at least one follow-up visit within a target window. Present cohort size,
  retained patients, retention rate, and change versus baseline.
- ROI: Estimate incremental benefit from reduced missed appointments, faster
  triage, or lower manual review time. Present assumptions explicitly:
  `ROI = (benefit - cost) / cost`.
- SHAP Values: If a supervised model is added later, show global feature
  importance, local explanations for high-risk cases, and a short clinical
  caveat that SHAP explains model behavior, not causality.
- Severity Mix: Present Mild/Moderate/Severe/Extreme shares as both counts and
  percentages to avoid misleading small-sample interpretations.
- Cluster Profiles: Include average age, average Y-BOCS score, family-history
  rate, Extreme rate, and patient count for each segment.

## Recommended Decision Workflow

1. Validate incoming data before analysis.
2. Refresh patient features and cluster assignment.
3. Review cluster profiles and severity mix.
4. Confirm statistically meaningful group differences.
5. Convert findings into a care-operations recommendation with owner, expected
   impact, and measurement plan.
