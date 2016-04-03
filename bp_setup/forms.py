from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.forms import ValidationError
from django_auth_ldap3.backends import LDAPBackend
from django_auth_ldap3.conf import settings

from bp_cupid.models import (
    Student,
)

import logging
logger = logging.getLogger(__name__)


class BPAuthenticationForm(AuthenticationForm):
    """
    Unser eigenes Authentifizierungsformular für das BP.
    """
    def clean(self):
        """
        Wenn sich ein Student einloggen will, müssen wir ein lokales
        Studentenobjekt erzeugen, in der wir die BP-Vorlieben speichern. Die
        erforderlichen Daten holen wir uns mittels LDAP vom Rechenzentrum.
        """
        cleaned_data = super(self.__class__, self).clean()

        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        ldap_backend = LDAPBackend()
        ldap_user = ldap_backend.bind_ldap_user(username, password)

        # Falls kein LDAP User existiert, probieren wir lokal weiter:
        if not ldap_user:
            return cleaned_data

        # der lokale User müsste schon erzeugt worden sein
        user = User.objects.get(username=username)

        connection = ldap_user.connection
        search_filter = '({}={})'.format(settings.UID_ATTRIB, username)

        # so heißen die Attribute auf dem LDAP-Server:
        mat_nr_attr = 'sos-mtknr'
        gender_attr = 'uniRGender'

        attributes = ldap_backend.search_ldap(
            connection,
            search_filter,
            attributes=[mat_nr_attr, gender_attr],
            size_limit=1,
        )

        mat_nr = int(attributes[mat_nr_attr][0])
        weiblich = attributes[gender_attr][0] == 'W'

        """
        Hier holen wir das lokale Studentenobjekt und speichern die relevanten
        Daten. Leider sind ein paar Daten wie Name und E-Mail-Adresse redundant,
        aber was willste machen.
        """
        try:
            student = Student.objects.get(mat_nr=mat_nr)
            student.user = user
            student.name = user.last_name
            student.vorname = user.first_name
            student.email = user.email
            student.weiblich = weiblich
            student.save()
        except Student.DoesNotExist:
            raise ValidationError(
                'Nicht zugelassen.'
            )

        return cleaned_data
