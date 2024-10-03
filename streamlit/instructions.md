# Streamlit Dashboard Overview

### 1. **Dashboard Pages**

We will create five pages, each corresponding to points 2–6 of [this document](https://docs.google.com/document/d/1uoX99WIjO-dI-5h3vfyuhd81wzdV7-1VuEM3KC5qMko/edit#heading=h.xdt1zh64eu0a). Each page will focus on a specific dataset, allowing users to explore and understand the data effectively.

### 2. **Datasets**

For each page, we will use specific datasets provided in the [NASA Space Apps 2024 challenge](https://www.spaceappschallenge.org/nasa-space-apps-2024/challenges/uncover-the-role-of-greenhouse-gases-in-your-neighborhood/?tab=resources). These datasets will be visualized in a way that highlights key insights.

### 3. **Map Visualization**

Initially, we will display a generic map. On this map, users will be able to see data relevant to the page’s focus, similar to the approach used in the `5_Natural_Emissions_and_Sinks.py` file.

### 4. **Toggle Between Datasets**

Users can toggle between different datasets using checkboxes on the map. This feature will allow them to compare various datasets interactively.

### 5. **Short Descriptions**

Above the map, a brief description will provide context for the data shown on the page. This will help users understand what they are viewing without overwhelming them with details.

### 6. **Global Statistics**

We will display global statistics, showing comparisons between the datasets. To achieve this, we will generate data as outlined in the "Generate Whole World Data" section and show a detailed comparison for each page, enhancing the decision-making impact.

---

### **Generate Whole World Data**

1. Follow the instructions in the `data/generate_data.py` script to create a global dataset.
2. Using the **monthly/yearly** data, we will showcase the global impact and comparisons, taking advantage of the information provided by GPT XD for additional insights.
3. In the dashboard, global statistics will be displayed similarly to the demo shown in the `7_Show_Data.py` script. Instead of just showing one data point, we will present a comparison between multiple datasets to add depth to the analysis.
