
# Logistics Operations: Diagnostic Analysis Report

## :clipboard: Project Overview

This project performs a deep-dive diagnostic analysis into delivery efficiency for Olist| Brazilian E-Commerce. The goal is to identify why specific orders experience extreme delays ("long-tail outliers") and to provide data-driven recommendations for operational improvement.




## :bar_chart: Data Source

The analysis is based on the Olist Brazilian E-Commerce Dataset, which contains information on approximately 100,000 orders from 2016 to 2018.

**Dataset Origin:** [Kaggle - Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)
 

**Data Volume:** 100k+ orders across 73 product categories.

**Key Features utilized:** Order timestamps, customer/seller location, freight value, and product dimensions.
## :hammer_and_wrench: Tech Stack

**Language:** Python 3.10+

**Data Manipulation:** pandas, numpy

**Spatial Analysis:** geopandas, h3

**Statistical Testing:** scipy.stats (Chi-Squared, Correlation analysis)

**Visualization:** matplotlib, seaborn, folium
## :file_folder: Analysis Report

**[Data Hygiene](notebooks/data_hygiene.ipynb)**: Auditing for batch updates and identifying reporting lag patterns.

**[Temporal Analysis](notebooks/temporal_analysis.ipynb):** An evaluation of systemic operations, identifying a rigid midday-to-midnight delivery schedule. Featuring a comparative gap analysis of order registration vs final delivery volume.

**[Regional Performance & Velocity](notebooks/regional_performance.ipynb):** The "Velocity Paradox" at the state and regional levels. A comparison of raw delivery times vs. normalized speed ($km/hr$) across the 5 main Brazilian regions.

**[Deep Dive: SP & RJ Analysis](notebooks/sp_rj.ipynb):** Municipality-level friction mapping for São Paulo and Rio de Janeiro. Identification of "Logistics Sinks" in low-volume areas and the impact of island geography on delivery efficiency.

**[Attribute Testing](notebooks/attribute_testing.ipynb):** Testing the impact of product attributes(weight, lenght, width, height), and distance(seller to customer) on delivery time.

## :mag: Key Findings

1. **The Weekend Operational Standstill**\
Data reveals a near-total cessation of logistics activity during weekends.
   * **Acceptance Gap:** Saturday volume is only ~10% of weekday levels. Remarkably, only 36 orders were accepted on Sundays across all 27 states over the 3-year period.
   * **Delivery Dead Zone:** Sunday deliveries are nearly non-existent. This 48-hour pause triggers a 12-day cascading penalty for Sunday orders; buried by Monday’s fresh volume (FIFO failure), a brief pause becomes a major delay.

2. **The "Late-Shift" Inefficiency**\
Data reveals a rigid, late-leaning delivery window from **12:00 PM to 12:00 AM**.
   * **Sorting Lag**: Starting deliveries at midday suggests that local hubs spend the most productive morning hours on internal sorting rather than transit.

   * **Customer Friction**: Ending the window at midnight likely conflicts with residential sleep norms, suggesting the "last-mile" is struggling to clear daily volume within standard hours.

3. **The Velocity Paradox: Long-Haul vs. Urban Friction**\
Regional analysis proves that "Total Days" is a misleading metric:
   * **High-Velocity North**: Despite long durations, the North is highly efficient over distance.
   * **Low-Velocity South-East**: Areas closest to hubs have the lowest velocity. This signals intense urban friction (traffic and high-density drop-offs). The current midday start likely forces drivers into peak afternoon traffic, further degrading speed.

4. **Routing-Driven "Logistics Sinks"**\
Low-volume and island municipalities (specifically in RJ) face severe delays. These areas lack the volume for frequent dispatches, forcing orders to wait at hubs for "batch routing" regardless of when the customer ordered.

5. **Product Attribute Neutrality**\
Analysis showed **no strong correlation** between product weight, dimensions, and delivery speed. Bottlenecks are entirely **Schedule and Process-driven**, not cargo-dependent.

## :rocket: Strategic Recommendations

1. **Shift Dispatch to "Early-Bird" Hours**: Move the local hub sorting process to night shifts to allow drivers to depart by 8:00 AM. This would bypass peak afternoon traffic and ensure deliveries are completed by a customer-friendly 8:00 PM cutoff.

2. **Enforce FIFO Priority**: Implement a strict First-In, First-Out rule for Monday mornings to ensure weekend backlogs are processed before new Monday arrivals.

3. **Scheduled vs. Volume-Based Routing**: For "orphan" municipalities in SP and RJ, transition from volume-based dispatch (waiting for a full truck) to a fixed-schedule rotation to eliminate long-tail wait times.
## :crystal_ball: Future Work

1. **Predictive Modeling (Regression Analysis)**
Build a Multiple Linear Regression model to quantify the exact weight of the "Sunday Penalty" on delivery timelines.


## :bust_in_silhouette: Author

Saw Yu Nwe

Project Status: Phase 1 (Diagnostic) Complete | Phase 2 (Predictive & Automation) In Progress.
