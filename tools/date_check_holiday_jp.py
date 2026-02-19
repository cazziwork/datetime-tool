from datetime import datetime
from typing import Any, Generator

import pytz
from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from .holiday_cache import get_holiday_name

WEEKDAY_JP = ["月曜日", "火曜日", "水曜日", "木曜日", "金曜日", "土曜日", "日曜日"]


class IsHolidayJpTool(Tool):
    def _invoke(
        self, tool_parameters: dict[str, Any]
    ) -> Generator[ToolInvokeMessage, None, None]:
        date_str = tool_parameters.get("date") or ""
        tz_name = tool_parameters.get("timezone") or "Asia/Tokyo"

        try:
            tz = pytz.timezone(tz_name)
        except pytz.UnknownTimeZoneError:
            yield self.create_text_message(f"Unknown timezone: {tz_name}")
            return

        if date_str:
            try:
                for fmt in ("%Y-%m-%d", "%Y/%m/%d"):
                    try:
                        target = datetime.strptime(date_str, fmt).date()
                        break
                    except ValueError:
                        continue
                else:
                    raise ValueError(f"Invalid date format: {date_str}")
            except ValueError as e:
                yield self.create_text_message(str(e))
                return
        else:
            target = datetime.now(tz).date()

        holiday_name = get_holiday_name(target)
        is_holiday = holiday_name is not None
        is_weekend = target.weekday() >= 5
        is_business_day = not is_holiday and not is_weekend

        output = {
            "date": target.isoformat(),
            "is_holiday": is_holiday,
            "holiday_name": holiday_name,
            "is_weekend": is_weekend,
            "is_business_day": is_business_day,
            "day_of_week": WEEKDAY_JP[target.weekday()],
        }

        yield self.create_json_message(output)
        yield self.create_variable_message("date", output["date"])
        yield self.create_variable_message("is_holiday", output["is_holiday"])
        yield self.create_variable_message("holiday_name", output["holiday_name"] or "")
        yield self.create_variable_message("is_weekend", output["is_weekend"])
        yield self.create_variable_message("is_business_day", output["is_business_day"])
        yield self.create_variable_message("day_of_week", output["day_of_week"])
