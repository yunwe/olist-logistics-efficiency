
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

**EDA & Data Hygiene**: Auditing for batch updates and identifying reporting lag patterns.

**Temporal Analysis**: Investigating the Sunday 12-day penalty and weekday delivery windows.

**Spatial Velocity & Mapping**: GeoPandas mapping of SP and RJ and calculating the "Velocity Paradox" across regions.

**Product & Attribute Testing**: Testing the impact of weight and dimensions on delivery time.
## :mag: Key Findings

1. **The Sunday "FIFO" Failure**

Orders reaching carriers on Sunday suffer a **double mean delivery time (12 days)**. Because the system pauses on weekends, Sunday orders are likely buried by fresh Monday volume. This **First-In, Last-Out (FILO)** behavior turns a 48-hour weekend break into a massive 12-day customer penalty.

2. **The "Late-Shift" Inefficiency**
Data reveals a rigid, late-leaning delivery window from **12:00 PM to 12:00 AM**.

* **Sorting Lag**: Starting deliveries at midday suggests that local hubs spend the most productive morning hours on internal sorting rather than transit.

* **Customer Friction**: Ending the window at midnight likely conflicts with residential sleep norms, suggesting the "last-mile" is struggling to clear daily volume within standard hours.

3. **The Velocity Paradox: Long-Haul vs. Urban Friction**
Regional analysis proves that "Total Days" is a misleading metric:

* **High-Velocity North**: Despite long durations, the North is highly efficient over distance.

* **Low-Velocity South-East**: Areas closest to hubs have the lowest velocity. This signals intense urban friction (traffic and high-density drop-offs). The current midday start likely forces drivers into peak afternoon traffic, further degrading speed.

4. **Routing-Driven "Logistics Sinks"**
Low-volume and island municipalities (specifically in SP and RJ) face severe delays. These areas lack the volume for frequent dispatches, forcing orders to wait at hubs for "batch routing" regardless of when the customer ordered.

5. **Product Attribute Neutrality**
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
