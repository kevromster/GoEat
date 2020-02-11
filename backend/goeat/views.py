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
"""DRF views."""


from rest_framework import viewsets

from goeat import models
from goeat import serializers


class TrackingNodeViewSet(viewsets.ModelViewSet):
    queryset = models.TrackingNode.objects.all()
    serializer_class = serializers.TrackingNodeSerializer

    def get_queryset(self):
        tg_chat_id = self.request.query_params.get('tgChatId', None)
        result = models.TrackingNode.objects.all()

        if tg_chat_id is not None:
            result = result.filter(tg_chat_id=tg_chat_id)

        return result
