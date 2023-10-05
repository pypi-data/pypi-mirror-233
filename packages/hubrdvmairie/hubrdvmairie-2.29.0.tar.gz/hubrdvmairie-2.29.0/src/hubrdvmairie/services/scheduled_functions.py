import asyncio
import logging

from unidecode import unidecode

from ..db.utils import get_all_editors, set_all_meeting_points


async def run_daily_scheduled_functions():
    """function that collecte meeting point from editor"""
    _logger = logging.getLogger("root")
    try:
        meeting_point_list = []
        editor_futures = []
        for editor in get_all_editors():
            editor_futures.append(
                asyncio.ensure_future(editor.get_managed_meeting_points())
            )
        all_results = await asyncio.gather(*editor_futures)

        for editor_result in all_results:
            meeting_point_list += editor_result
        point_index = 201
        for point in meeting_point_list:
            point["id"] = str(point_index)
            point["decoded_city_name"] = (
                unidecode(point["city_name"])
                .replace(" ", "-")
                .replace("'", "-")
                .lower()
            )
            point_index += 1
        set_all_meeting_points(meeting_point_list)
    except Exception as daily_sch_e:
        _logger.error("Error while running daily scheduled functions : %s", daily_sch_e)
