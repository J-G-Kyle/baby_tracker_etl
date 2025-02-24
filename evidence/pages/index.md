---
title: Baby Data Dashboard
---

```sql age_months
    SELECT DATEDIFF('month', '2024-09-03', CURRENT_DATE) as age_months
```
### Current Age

<BigValue 
  data={age_months} 
  value=age_months
  title="Age in months"
/>

### Nappies by frequency and type

When your baby is breastfed it's much more difficult to track what is going into them. The simpler method for 
assessing if they are getting enough nutrition is to track what is leaving them instead. Our baby has CMPA, so we 
went through a period of eliminating dairy to try and improve their health.

```sql diapers
  select
      *
  from baby.diaper
  order by date, timestamp
```

<Dropdown data={diapers} name=status value=status>
    <DropdownOption value="%" valueLabel="All Categories"/>
</Dropdown>

<Dropdown name=year>
    <DropdownOption value="%" valueLabel="All Years"/>
    <DropdownOption value=2025/>
    <DropdownOption value=2024/>
</Dropdown>


```sql diapers_by_type
  select 
      date,
      status, COUNT(status) as count
  from baby.diaper
  where status like '${inputs.status.value}'
  and date_part('year', date) like '${inputs.year.value}'
  group by date, status
  order by date desc
```

```sql diapers_by_type_dirty
  select 
      date,
      status, COUNT(status) as count
  from baby.diaper
  where status in ('Dirty', 'Mixed')
  group by date, status
  order by date desc
```

<BarChart
    data={diapers_by_type}
    title="Daily nappies by type {inputs.category.label}"
    x=date
    y=count
    series=status>
<ReferenceArea xMin='2024-10-16' xMax='2024-11-16' label="Dairy Elimination" color=warning/>
</BarChart>

<CalendarHeatmap
    data={diapers_by_type_dirty}
    date=date
    value=count
    title="Dirty Nappies Heatmap"
    subtitle="Count and Frequency of Poops"
/>

```sql sleep_duration
SELECT
    date,
    SUM(CASE
            WHEN date_part('hour', timestamp) >= 20 OR date_part('hour', timestamp) < 09
            THEN duration_min
            ELSE 0
        END) AS night_minutes,
    SUM(CASE
            WHEN date_part('hour', timestamp) >= 09 AND date_part('hour', timestamp) < 20
            THEN duration_min
            ELSE 0
        END) AS day_minutes
FROM sleep
GROUP BY date
ORDER BY date
```

```sql sleep_duration_categories
SELECT
    date,
    ROUND((SUM(CASE
            WHEN date_part('hour', timestamp) >= 20 OR date_part('hour', timestamp) < 09
            THEN duration_min
            ELSE 0
        END))/60, 1) AS duration,
    'night' AS category,
FROM sleep
GROUP BY date

UNION ALL

SELECT
    date,
    ROUND((SUM(CASE
            WHEN date_part('hour', timestamp) >= 09 AND date_part('hour', timestamp) < 20
            THEN duration_min
            ELSE 0
        END))/60, 1) AS duration_day,
    'day' AS category
FROM sleep
GROUP BY date
ORDER BY date;
```

### Duration of sleep

Newborns can sleep up to 18 hours a day, and as they age it is expected that their time awake during the day will 
get longer.

<AreaChart
    data={sleep_duration_categories}
    x=date
    y=duration
    series=category
    title="Hours of sleep during day & night"
    yFmt="num0">
<ReferenceArea xMin='2024-10-16' xMax='2024-11-16' label="Dairy Elimination" color=warning/>
</AreaChart>

```sql number_of_night_wakes
SELECT 
    date,
    COUNT(CASE
            WHEN date_part('hour', timestamp) >= 20 OR date_part('hour', timestamp) < 09
            THEN 1
            ELSE 0
        END) AS count_wakes,
    'night' AS category,
FROM sleep
GROUP BY date
ORDER BY date
```

As they grow older the number of times they wake up during the night should decrease as well. This chart is mainly 
to elicit sympathy from those without children, however.

<BarChart 
    data={number_of_night_wakes}
    x=date
    y=count_wakes
    title="Number of wakes at night"
    subtitle="Number of wakes at night"
/>

### Feeding

Babies are voracious eaters, and though they get more efficient at eating as they grow it remains an all consuming 
process to keep them satisfied.

```sql nursing_mean_by_day
select avg(total_duration_min) as mean_duration, date, start_side, count(date) as number_of_feeds
from nursing
where start_side IS NOT null
group by date, start_side
order by date, start_side
```

<LineChart 
    data={nursing_mean_by_day}
    x=date
    y=mean_duration 
    yAxisTitle="Minutes Feeding"
    series=start_side
    title="Mean feed duration by day"
/>

<BarChart 
    data={nursing_mean_by_day}
    x=date
    y=number_of_feeds
    yAxisTitle="Number of Feeds"
    title="Number of Feeds per day"
/>

```sql nursing_total
select SUM(total_duration_min)/60 as total_duration_hours
from nursing
where start_side IS NOT null
```

Our baby's feeds were on the shorter side, but they still add up to a huge amount of time.

<BigValue 
  data={nursing_total} 
  value=total_duration_hours
  title="Hours spent feeding"
/>

### Growth

One of the key metrics for assessing if your baby is thriving or not is their weight. It's tracked manually in a red 
booklet by the health visitor, but keeping an electronic record and measuring more often gave us peace of mind about 
our baby's growth.

```sql weight
select date, weight_kg from growth
where weight_kg is not null
```

<LineChart
    data={weight}
    x=date
    y=weight_kg
    yAxisTitle="Weight in kg"
    title="Growth in kg"
/>

### More Info
- For the background of this project see [Medium](https://www.medium.com/placeholder)
- All files available on [Github](https://github.com/J-G-Kyle/baby_tracker_etl)

### Want to edit this page?
- Edit `evidence/pages/index.md` in the mounted directory
- Or add new markdown files in the `pages` folder

### Get Support
- Message us on [Slack](https://slack.evidence.dev/)
- Read the [Docs](https://docs.evidence.dev/)
- Open an issue on [Github](https://github.com/evidence-dev/evidence)
