---
name: data-visualization
description: Use when analyzing a dataset, choosing a chart, specifying a dashboard, or implementing an accessible Streamlit visualization.
---

# Data visualization

## Procedure

1. Write the user question and the decision the visualization supports.
2. Inspect schema, grain, types, ranges, missingness, duplicates, outliers, and time coverage.
3. Define measures, dimensions, filters, aggregation, and uncertainty.
4. Choose the visual encoding:
   - comparison: bar or dot plot
   - trend: line chart
   - distribution: histogram, box, violin, or ECDF
   - relationship: scatter plot
   - part-to-whole: stacked bar when categories are limited
   - geography: map only when location is analytically meaningful
5. Add titles, units, sources, definitions, and annotations.
6. Check truthful scales, accessible colors, non-color cues, keyboard use, and text alternatives.
7. Validate the chart against known values and the original question.

Record the result in `docs/templates/visualization-spec.md`.

