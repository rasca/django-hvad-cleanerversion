# -*- coding: utf-8 -*-

from versions.models import Versionable, VersionManager, VersionedQuerySet
from hvad.manager import TranslationManager, TranslationQueryset
from hvad.models import TranslatableModel


class TranslationVersionQueryset(TranslationQueryset, VersionedQuerySet):
    pass


class TranslatableVersionManager(TranslationManager, VersionManager):
    """
    Manager for cleanerversion + hvad
    """

    queryset_class = TranslationVersionQueryset
    default_class = VersionedQuerySet


class TranslatableVersionableModel(TranslatableModel, Versionable):
    objects = TranslatableVersionManager()
    _base_manager = VersionManager()


    def clone_with_translations(self, forced_version_date=None):
        new_instance = self.clone(forced_version_date)
        for translation in new_instance.translations.all():
            translation.pk = None
            translation.id = None
            translation.master = self
            translation.save()
        return new_instance

    class Meta:
        abstract = True


class WithVersionedRelationsMixin(object):

    def get_versioned_relation(self, relation, as_of):
        # get the model from the relation
        field = self._meta.get_field(relation)
        related_model = field.related_model
        related_id = getattr(self, '%s_id' % field.name)

        if issubclass(related_model, TranslatableModel): # if it's translatable
            # return the as_of with fallbacks
            versioned = related_model.objects.as_of(as_of).get(identity=related_id)
            fallback = related_model.objects.language().fallbacks().get(pk=versioned.pk)
            return related_model.objects.adjust_version_as_of(fallback, as_of)
        else: # if it's no translatable
            # return the as_of
            return field.related_model.objects.as_of(as_of).get(identity=related_id)

