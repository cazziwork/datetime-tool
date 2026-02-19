# DateTime Tool

## Overview

DateTime Tool is a Dify plugin that provides date and time manipulation utilities
with Japanese holiday support. It includes tools for relative date calculation,
month boundary detection, and Japanese holiday checking.

## Features

- **Relative Date Calculation**: Add or subtract days, weeks, months, or years
  from a date
- **Business Day Support**: Skip weekends and Japanese public holidays when
  calculating dates
- **Month Boundaries**: Get the first or last day of any month
- **Japanese Holiday Check**: Determine if a date is a Japanese public holiday
  or business day
- **Timezone Support**: All tools support configurable timezones (default:
  Asia/Tokyo)

## Tools

### 1. Add Duration to Date (`date_add`)

Calculate a future or past date by adding or subtracting a duration from a base
date.

**Parameters:**

- `date` (required): Base date in `YYYY-MM-DD` format
- `amount` (required): Number of units to add (use negative values to subtract)
- `unit` (required): `day`, `week`, `month`, or `year`
- `business_days_only` (optional, default: `false`): When `true` and unit is
  `day`, only count business days (skips weekends and Japanese public holidays)
- `timezone` (optional, default: `Asia/Tokyo`): Timezone name

**Output:**

| Field                | Type    | Description                            |
| -------------------- | ------- | -------------------------------------- |
| `result_date`        | string  | Calculated date in `YYYY-MM-DD` format |
| `base_date`          | string  | Input base date                        |
| `amount`             | number  | Amount added                           |
| `unit`               | string  | Unit used                              |
| `business_days_only` | boolean | Whether business days mode was used    |

**Example:**

```
date: "2025-02-19", amount: 10, unit: "day"
→ result_date: "2025-03-01"

date: "2025-02-19", amount: 10, unit: "day", business_days_only: true
→ result_date: "2025-03-05" (skips weekends and holidays)

date: "2025-02-19", amount: -3, unit: "month"
→ result_date: "2024-11-19"
```

---

### 2. Get Month Start/End (`date_month_edge`)

Get the first or last day of a month.

**Parameters:**

- `date` (optional): Reference date in `YYYY-MM-DD` format (defaults to today)
- `edge` (required): `start` (first day) or `end` (last day)
- `timezone` (optional, default: `Asia/Tokyo`): Timezone name

**Output:**

| Field         | Type   | Description                        |
| ------------- | ------ | ---------------------------------- |
| `result_date` | string | Result date in `YYYY-MM-DD` format |
| `edge`        | string | `start` or `end`                   |
| `year`        | number | Year of the result                 |
| `month`       | number | Month of the result                |

**Example:**

```
date: "2025-02-19", edge: "start"
→ result_date: "2025-02-01"

date: "2025-02-19", edge: "end"
→ result_date: "2025-02-28"
```

---

### 3. Check Japanese Holiday (`date_check_holiday_jp`)

Check if a date is a Japanese public holiday or business day.

Uses the official Japanese Cabinet Office holiday data, fetched and cached
locally for 24 hours.

**Parameters:**

- `date` (optional): Date to check in `YYYY-MM-DD` format (defaults to today)
- `timezone` (optional, default: `Asia/Tokyo`): Timezone name

**Output:**

| Field             | Type    | Description                                                     |
| ----------------- | ------- | --------------------------------------------------------------- |
| `date`            | string  | The date checked in `YYYY-MM-DD` format                         |
| `is_holiday`      | boolean | `true` if the date is a Japanese public holiday                 |
| `holiday_name`    | string  | Name of the holiday in Japanese (`null` if not a holiday)       |
| `is_weekend`      | boolean | `true` if the date is Saturday or Sunday                        |
| `is_business_day` | boolean | `true` if the date is a business day (not a weekend or holiday) |
| `day_of_week`     | string  | Day of the week in Japanese (e.g., `月曜日`)                    |

**Example:**

```
date: "2025-01-01"
→ is_holiday: true, holiday_name: "元日", is_weekend: false, is_business_day: false

date: "2025-02-17"  (Monday)
→ is_holiday: false, holiday_name: null, is_weekend: false, is_business_day: true
```

---

## Common Use Cases

### 1. Calculate Deadline

Calculate a deadline N business days from today:

```
date_add: date="2025-02-19", amount=5, unit="day", business_days_only=true
→ result_date: "2025-02-26"
```

### 2. Get This Month's Boundaries

Get the start and end of the current month:

```
date_month_edge: edge="start"  → "2025-02-01"
date_month_edge: edge="end"    → "2025-02-28"
```

### 3. Check Before Scheduling

Verify a date is a business day before scheduling:

```
date_check_holiday_jp: date="2025-02-11"
→ is_holiday: true, holiday_name: "建国記念の日", is_business_day: false
```

---

## Requirements

- **Python**: 3.12 or higher
- **Dify Version**: Compatible with Dify plugin system
- **Dependencies**: pytz, python-dateutil, requests (automatically installed)

## Privacy

See [PRIVACY.md](PRIVACY.md) for privacy and data handling information.

## Contributing

For bug reports or feature requests, please contact the author: cazziwork

## Changelog

### Version 0.0.1

- Initial release
- Tools: `date_add`, `date_month_edge`, `date_check_holiday_jp`
- Japanese holiday data from Cabinet Office (cached 24 hours)
- Business day mode in `date_add`
