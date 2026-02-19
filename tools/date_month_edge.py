import calendar
from datetime import date, datetime
from typing import Any, Generator

import pytz
from dateutil.relativedelta import relativedelta
from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage


class GetMonthEdgeTool(Tool):
    def _invoke(
        self, tool_parameters: dict[str, Any]
    ) -> Generator[ToolInvokeMessage, None, None]:
        date_str = tool_parameters.get("date") or ""
        edge = tool_parameters.get("edge", "start")
        offset_months = int(tool_parameters.get("offset_months", 0))
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
                        base = datetime.strptime(date_str, fmt).date()
                        break
                    except ValueError:
                        continue
                else:
                    raise ValueError(f"Invalid date format: {date_str}")
            except ValueError as e:
                yield self.create_text_message(str(e))
                return
        else:
            base = datetime.now(tz).date()

        # オフセット適用
        target = base + relativedelta(months=offset_months)

        if edge == "start":
            result = date(target.year, target.month, 1)
        elif edge == "end":
            last_day = calendar.monthrange(target.year, target.month)[1]
            result = date(target.year, target.month, last_day)
        else:
            yield self.create_text_message(
                f"Invalid edge '{edge}'. Must be 'start' or 'end'."
            )
            return

        output = {
            "result_date": result.isoformat(),
            "edge": edge,
            "year": result.year,
            "month": result.month,
        }

        yield self.create_json_message(output)
        yield self.create_variable_message("result_date", output["result_date"])
        yield self.create_variable_message("edge", output["edge"])
        yield self.create_variable_message("year", output["year"])
        yield self.create_variable_message("month", output["month"])
