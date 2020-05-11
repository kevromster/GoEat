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
"""DRF serializers."""


from rest_framework import serializers
from goeat import models


class TrackingNodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TrackingNode
        fields = ['id', 'date_created', 'tg_chat_id', 'camera_url', 'time_range_start', 'time_range_finish']
        read_only_fields = ('date_created',)
