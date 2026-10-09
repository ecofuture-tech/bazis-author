# Copyright 2026 EcoFuture Technology Services LLC and contributors
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

"""
The admin of an `AuthorAdminMixin` model: its changelist shows the autocomplete filter by
author and filters by it.
"""

from django.test import Client

import pytest
from entity.models import ParentEntity

from bazis.contrib.users import get_user_model


User = get_user_model()

URL = '/admin/entity/parententity/'


@pytest.mark.django_db
def test_changelist_filters_by_author():
    admin = User.objects.create_superuser(
        'admin', email='admin@site.com', password='weak_password_1'
    )
    other = User.objects.create_user('other', email='other@site.com', password='weak_password_2')
    ParentEntity.objects.create(name='Own', author=admin, price='1.00')
    ParentEntity.objects.create(name='Other', author=other, price='1.00')
    client = Client()
    client.force_login(admin)

    def names(response):
        assert response.status_code == 200
        return {it.name for it in response.context['cl'].result_list}

    response = client.get(URL)
    assert names(response) == {'Own', 'Other'}
    assert 'id="id-author-dal-filter"' in response.content.decode()

    response = client.get(URL, {'author': str(other.pk)})
    assert names(response) == {'Other'}
    # the selected author is rendered in the filter
    assert f'<option value="{other.pk}" selected>other</option>' in response.content.decode()
