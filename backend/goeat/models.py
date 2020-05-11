# Copyright © 2020 Roman Kuskov. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
"""DRF models."""


from django.db import models


class TrackingNode(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    tg_chat_id = models.BigIntegerField()
    camera_url = models.CharField(max_length=2048, blank=False)

    # when to track the camera
    time_range_start = models.TimeField(blank=False)
    time_range_finish = models.TimeField(blank=False)

    def __str__(self):
        return f"tg_chat_id:{self.tg_chat_id}"

    class Meta:
        ordering = ['date_created']
