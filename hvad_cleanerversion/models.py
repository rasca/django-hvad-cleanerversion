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

    class Meta:
        abstract = True


def get_versioned_relation(instance, relation, as_of):
    """
    Gets a versioned relation with fallbacks

    Executes an extra query. Works for translatable and non translatable
    models.
    """
    # get the model from the relation
    field = instance._meta.get_field(relation)
    related_model = field.related_model
    related_id = getattr(instance, '%s_id' % field.name)

    if issubclass(related_model, TranslatableModel): # if it's translatable
        # return the as_of with fallbacks
        versioned = related_model.objects.as_of(as_of).get(identity=related_id)
        fallback = related_model.objects.language().fallbacks().get(pk=versioned.pk)
        return related_model.objects.adjust_version_as_of(fallback, as_of)
    else: # if it's no translatable
        # return the as_of
        return field.related_model.objects.as_of(as_of).get(identity=related_id)

def filter_versioned_relation(instance, relation):
    """
    Gets the related models with fallbacks
    """
    # get the model from the relation
    field = instance._meta.get_field(relation)
    related_model = field.related_model
    qs = getattr(instance, relation)

    if issubclass(related_model, TranslatableModel): # if it's translatable
        # return the as_of with fallbacks
        return qs.language().fallbacks().filter(version_end_date=instance.version_end_date)
    else: # if it's no translatable
        # return the as_of
        return qs.filter(version_end_date=instance.version_end_date)


def clone_with_translations(instance, forced_version_date=None):
    """
    Clones the given instance and it's relations

    Expects a TranslatableModel
    """
    new_instance = instance.clone(forced_version_date)
    for translation in new_instance.translations.all():
        translation.pk = None
        translation.id = None
        translation.master = instance
        translation.save()
    return new_instance
