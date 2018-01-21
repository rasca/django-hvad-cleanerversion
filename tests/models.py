from django.db import models

from versions.models import Versionable, VersionManager, VersionedForeignKey
from hvad.models import TranslatableModel, TranslatedFields

from hvad_cleanerversion.models import TranslatableVersionableModel


class RegularModel(models.Model):
    translated = models.ForeignKey('TranslatedModel', null=True)
    versioned = VersionedForeignKey('VersionedModel', null=True)
    versioned_regular = models.ForeignKey('VersionedModel', null=True)
    both = VersionedForeignKey('TranslatedVersionedModel', null=True)


class TranslatedModel(TranslatableModel):
    translations = TranslatedFields(
        name=models.CharField(max_length=255)
    )


class VersionedModel(Versionable):
    name = models.CharField(max_length=255)


class TranslatedVersionedModel(TranslatableVersionableModel):
    translations = TranslatedFields(
        name=models.CharField(max_length=255)
    )

class RelatedModel(TranslatableVersionableModel):
    origin = VersionedForeignKey('TranslatedVersionedModel', related_name='related')
    translations = TranslatedFields(
        name=models.CharField(max_length=255)
    )
