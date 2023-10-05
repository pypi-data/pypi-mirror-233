from collections import OrderedDict
from typing import List

from ewoksutils import event_utils

from ..utils import Resource
from .. import api
from ...events.ewoks_events import reader_context


class ExecutionEvents(Resource):
    @api.get_ewoks_events()
    def get(self, **filters) -> List[List[dict]]:
        jobs = OrderedDict()
        with reader_context() as reader:
            if reader is None:
                raise RuntimeError("server not configured for ewoks events")
            for event in reader.get_events(**filters):
                job_id = event["job_id"]
                if job_id not in jobs:
                    jobs[job_id] = list()
                if "engine" in event_utils.FIELD_TYPES:
                    event["binding"] = event["engine"]
                jobs[job_id].append(event)
        return {"jobs": list(jobs.values())}, 200
