

from django.core.urlresolvers import reverse

from rest_framework import status
from rest_framework.test import APITestCase
from django.test import RequestFactory, Client
from rest_framework.test import APIClient
from iati_synchroniser.factory import synchroniser_factory
from iati.permissions.factories import OrganisationGroupFactory, UserFactory, OrganisationAdminGroupFactory
from rest_framework.authtoken.models import Token

from iati_synchroniser.models import Publisher
from iati.permissions.models import OrganisationGroup

class TestOrganisationGroupAPI(APITestCase):
    rf = RequestFactory()
    c = APIClient()

    def test_add_user_to_organisation_group_fail(self):
        """
        Make sure adding a user to admin group fails when the user is not in the admin group
        """
        organisation_group = OrganisationGroupFactory.create()
        user = UserFactory.create(username='test1')
        new_user = UserFactory.create(username='test2')

        # organisation_group.user_set.add(user)

        self.c.force_authenticate(user)

        data = {
            "user_id": new_user.id,
        }

        res = self.c.post(
                "/api/publishers/{}/group/?format=json".format(organisation_group.publisher.id), 
                data,
                format='json'
                )

        self.assertEquals(res.status_code, 403)


    def test_add_user_to_organisation_group_success(self):
        """
        Adding a user to an admin group when the user is in the admin group
        """
        organisation_group = OrganisationGroupFactory.create()
        admin_group = OrganisationAdminGroupFactory.create()

        user = UserFactory.create(username='test1')
        new_user = UserFactory.create(username='test2')

        organisation_group.user_set.add(user)
        admin_group.user_set.add(user)

        admin_group.save()

        self.c.force_authenticate(user)

        data = {
            "user_id": new_user.id,
        }

        res = self.c.post(
                "/api/publishers/{}/group/?format=json".format(organisation_group.publisher.id), 
                data,
                format='json'
                )

        self.assertEquals(res.status_code, 200)
        self.assertEquals(len(OrganisationGroup.objects.get(pk=organisation_group.id).user_set.all()), 2)

    def test_remove_user_from_organisation_group_fail(self):
        """
        Make sure a normal user can't remove users from an admin group
        """
        organisation_group = OrganisationGroupFactory.create()
        user = UserFactory.create(username='test1')
        new_user = UserFactory.create(username='test2')

        # organisation_group.user_set.add(user)
        organisation_group.user_set.add(new_user)

        self.c.force_authenticate(user)

        data = {
            "user_id": new_user.id,
        }

        res = self.c.delete(
                "/api/publishers/{}/group/{}?format=json".format(organisation_group.publisher.id, new_user.id), 
                format='json'
                )

        self.assertEquals(res.status_code, 403)

    def test_remove_user_from_organisation_group_success(self):
        """
        Make sure a normal user can't remove users from an admin group
        """
        organisation_group = OrganisationGroupFactory.create()
        admin_group = OrganisationAdminGroupFactory.create()
        user = UserFactory.create(username='test1')
        new_user = UserFactory.create(username='test2')

        admin_group.user_set.add(user)
        organisation_group.user_set.add(user)
        organisation_group.user_set.add(new_user)

        self.c.force_authenticate(user)

        data = {
            "user_id": new_user.id,
        }

        res = self.c.delete(
                "/api/publishers/{}/group/{}?format=json".format(organisation_group.publisher.id, new_user.id), 
                format='json'
                )

        self.assertEquals(res.status_code, 200)


    def test_cant_remove_admin(self):
        """
        Before an admin can be removed from the organization, he must be removed from the organisation admin group
        """
        organisation_group = OrganisationGroupFactory.create()
        admin_group = OrganisationAdminGroupFactory.create()
        user = UserFactory.create(username='test1')
        new_user = UserFactory.create(username='test2')

        admin_group.user_set.add(user)
        organisation_group.user_set.add(user)

        admin_group.user_set.add(new_user)
        organisation_group.user_set.add(new_user)

        self.c.force_authenticate(user)

        res = self.c.delete(
                "/api/publishers/{}/group/{}?format=json".format(organisation_group.publisher.id, new_user.id), 
                format='json'
                )

        self.assertEquals(res.status_code, 401)
