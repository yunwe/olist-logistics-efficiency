# Logistics Operations: Diagnostic Analysis Report

## Project Overview
This project performs a deep-dive diagnostic analysis into delivery efficiency for a logistics dataset. The goal is to identify why specific orders experience extreme delays ("long-tail outliers") and to provide data-driven recommendations for operational improvement.

## Findings
### 1. Data Integrity & Reporting Behavior
Before analyzing physical delays, we audited the data for digital recording errors to ensure the "lateness" was real.
* Human Reporting Lag (The "Clean-Up" Effect): We found a statistically significant link between late orders and late-night timestamps (_p_-value: $4.6 x 10^{-18}$). This suggests drivers are physically delivering earlier but closing out orders in the app at the end of their shifts.
* Systemic Batching Audit: We checked for identical consecutive timestamps (System Batching).
    * Finding: No systemic batching was found.
    * Conclusion: Delays are driven by manual human behavior or physical logistics rather than automated system pulses.
* Process Instability: All product categories showed a Coefficient of Variation (CV) above `0.50`, ranging up to `1.21`.
    * Insight: The entire operation is in a "high-variance" state, meaning delivery times are highly unpredictable regardless of what is being shipped.

### 2. Temporal Bottlenecks: The "Sunday Wall"
The timing of when an order reaches a carrier is the strongest predictor of delay.

* The Sunday Spike: Orders reaching the carrier on Sunday have a mean delivery time of `24.42` days— double the weekday mean of `12.05` days.

* The Accumulation Effect: Mean delivery times increase progressively as the week goes by.

    * Theory: Monday orders are dispatched first (First-In, First-Out). Unfinished orders from the weekend pile up, creating a "backlog wave" that peaks later in the week.

    * Heatmap Evidence: A Region vs. Weekday heatmap shows a "Dark Red" column for Sundays across all regions, confirming the bottleneck is a centralized carrier/processing issue rather than a local one.


### 3. Geographic Performance vs. Velocity
When looking at raw delivery hours, the map is misleading. We normalized the data using Velocity (Distance / Delivery Time) to find true efficiency.
| Region | Raw Performance (Days) | Velocity (km/hr) |
| --- | --- | --- |
| South-East | 11 days | 1.63 |
| South | 14 days | 2.33 |
| Central-West | 15 days | 3.05 |
| North-East | 20 days | 4.64 |
| North | 23 days | 5.16 |

* The Paradox: While the North has the longest delivery times, it actually has the highest velocity. This proves the North is efficient at moving goods over long distances, but the sheer distance is the "unavoidable" cause of the long duration.

* The South-East Problem: While the South-East is close to hubs (resulting in a short total duration), its low velocity indicates significant "Last-Mile" friction. This is likely driven by urban traffic congestion or a high volume of orders that exceeds current staffing levels.

### 4. Product Characteristics & Weight Categories
Investigated whether physical attributes drive delivery outliers.

* Dimensions & Weight: A correlation check between product weight, size dimensions, and delivery time revealed no strong relationship.

* Quadrant Analysis: An analysis of four weight categories showed an equal distribution across performance quadrants. This confirms that delays are not tied to product weight but are instead driven by overarching operational bottlenecks.

### 5. State Deep Dive: SP & RJ
We focused on São Paulo (SP) and Rio de Janeiro (RJ) as they represent the highest order volumes and the lowest velocities.

#### São Paulo (SP)
* The busiest municipalities maintain healthy delivery times.

* The slowest municipalities have very low order volumes, suggesting they lack dedicated local hubs and must wait for consolidated shipments.

#### Rio de Janeiro (RJ)
* Top Performer: Mangaratiba handles the largest total volume and operates the most efficient delivery hub.

* Infrastructure Challenges: As in SP, lower-volume areas suffer the most. Furthermore, many of the slowest areas in RJ are islands, which require multimodal transportation that creates a fixed, unavoidable delay.

## Technical Stack
Python (Pandas, NumPy)

Spatial Data: GeoPandas, h3

Visualization: Matplotlib, Seaborn, Folium

Statistics: SciPy

## Future Work (Phase 2)
* Predictive Modeling: Build a Regression Model (incorporating Distance, Region, and Freight Value) to predict delivery days.
