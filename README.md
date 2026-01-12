# Coffee Sales Analytics Platform

## Vision

Build a data-driven foundation for launching a successful coffee business by analyzing real coffee shop sales patterns, customer behavior, and product performance.

## Business Goals

1. **Understand Market Patterns** - When do people buy coffee? What sells best?
2. **Optimize Product Mix** - Which products drive revenue vs. traffic?
3. **Location Strategy** - What makes a coffee shop location successful?
4. **Pricing Intelligence** - How does pricing affect sales volume?
5. **Operational Planning** - Staff scheduling, inventory forecasting

## Project Phases

| Phase | Focus | Tools | Status |
|-------|-------|-------|--------|
| 1 | Data Exploration & Analysis | Databricks | **Current** |
| 2 | Data Transformation Pipeline | dbt | Planned |
| 3 | Automated Data Ingestion | Airbyte | Planned |
| 4 | Dashboard & Reporting | Databricks SQL | Planned |
| 5 | Predictive Analytics | ML Models | Future |

## Datasets

### 1. Coffee Shop Sales Dataset
**Source:** [Kaggle - Coffee Shop Sales](https://www.kaggle.com/datasets/ahmedmohamedibrahim1/coffee-shop-sales-dataset)

Transaction-level sales data for operational analysis:
- Transaction details (ID, date, time)
- Store information (location, unit)
- Product details (category, type, name, price)
- Time dimensions (month, day, weekday, hour)

### 2. Coffee Reviews Dataset
**Source:** [Kaggle - Coffee Reviews](https://www.kaggle.com/datasets/schmoyote/coffee-reviews-dataset)

Product quality and sourcing data for supplier/menu decisions:
- Coffee name and roaster
- Roast level (Light to Dark)
- Bean origin (country)
- Price per 100g (USD)
- Expert ratings
- Tasting notes and reviews

## Project Structure

```
coffee-sales-analysis/
├── README.md                    # This file
├── docs/
│   ├── STRATEGY.md             # Business strategy & insights
│   └── DATABRICKS_GUIDE.md     # Step-by-step Databricks tutorial
├── notebooks/                   # Databricks notebook exports
│   └── (exported .dbc or .py files)
├── dbt/                        # Future: dbt project
└── airbyte/                    # Future: Airbyte configs
```

## Documentation

- [Business Strategy](docs/STRATEGY.md) - Market analysis framework and insights
- [Databricks Guide](docs/DATABRICKS_GUIDE.md) - Step-by-step tutorial

## Key Questions to Answer

### Customer Behavior
- [ ] What are peak sales hours?
- [ ] How do weekdays compare to weekends?
- [ ] What's the average transaction value?

### Product Performance
- [ ] What are the top 10 selling products?
- [ ] Which category generates most revenue?
- [ ] What products have highest margins?

### Location Analysis
- [ ] Which locations perform best?
- [ ] Are there location-specific preferences?
- [ ] What correlates with high-performing stores?

### Business Planning
- [ ] What's the revenue per hour by location?
- [ ] How should staffing align with traffic?
- [ ] What inventory levels are needed?

### Sourcing & Quality (Reviews Dataset)
- [ ] What roast levels have highest ratings?
- [ ] Which origins offer best value (rating vs price)?
- [ ] What flavor profiles are trending?
- [ ] Which roasters have consistently high ratings?

## Getting Started

1. Read the [Business Strategy](docs/STRATEGY.md) to understand what we're solving
2. Follow the [Databricks Guide](docs/DATABRICKS_GUIDE.md) to set up and analyze data
3. Document your findings back into the strategy document
