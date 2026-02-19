from datetime import date, timedelta
from typing import Any, Generator

import pytz
from dateutil.relativedelta import relativedelta
from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from .holiday_cache import get_holiday_name


def _parse_date(date_str: str) -> date:
    from datetime import datetime
    for fmt in ("%Y-%m-%d", "%Y/%m/%d"):
        try:
            return datetime.strptime(date_str, fmt).date()
        except ValueError:
            continue
    raise ValueError(f"Invalid date format: {date_str}")


def _add_business_days(base: date, amount: int) -> date:
    """土日・祝日を除いた営業日を加算（負数で減算）。"""
    direction = 1 if amount >= 0 else -1
    remaining = abs(amount)
    current = base

    while remaining > 0:
        current += timedelta(days=direction)
        # 土日チェック
        if current.weekday() >= 5:
            continue
        # 祝日チェック
        if get_holiday_name(current) is not None:
            continue
        remaining -= 1

    return current


class AddDurationTool(Tool):
    def _invoke(
        self, tool_parameters: dict[str, Any]
    ) -> Generator[ToolInvokeMessage, None, None]:
        date_str = tool_parameters.get("date", "")
        amount = int(tool_parameters.get("amount", 0))
        unit = tool_parameters.get("unit", "day")
        business_days_only = bool(tool_parameters.get("business_days_only", False))
        tz_name = tool_parameters.get("timezone") or "Asia/Tokyo"

        try:
            pytz.timezone(tz_name)
        except pytz.UnknownTimeZoneError:
            yield self.create_text_message(f"Unknown timezone: {tz_name}")
            return

        try:
            base = _parse_date(date_str)
        except ValueError as e:
            yield self.create_text_message(str(e))
            return

        if business_days_only and unit == "day":
            result = _add_business_days(base, amount)
        else:
            delta_map = {
                "day": relativedelta(days=amount),
                "week": relativedelta(weeks=amount),
                "month": relativedelta(months=amount),
                "year": relativedelta(years=amount),
            }
            if unit not in delta_map:
                yield self.create_text_message(
                    f"Invalid unit '{unit}'. Must be one of: day, week, month, year."
                )
                return
            result = base + delta_map[unit]

        output = {
            "result_date": result.isoformat(),
            "base_date": base.isoformat(),
            "amount": amount,
            "unit": unit,
            "business_days_only": business_days_only,
        }

        yield self.create_json_message(output)
        yield self.create_variable_message("result_date", output["result_date"])
        yield self.create_variable_message("base_date", output["base_date"])
        yield self.create_variable_message("amount", output["amount"])
        yield self.create_variable_message("unit", output["unit"])
        yield self.create_variable_message("business_days_only", output["business_days_only"])
