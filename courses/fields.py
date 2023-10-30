from django.db import models
from django.core.exceptions import ObjectDoesNotExist


class OrderField(models.PositiveIntegerField):
    def __init__(self, for_fields=None, *args, **kwargs):
        # for_fields'- indicate the fields that the order has to be calculated with respect to.
        self.for_fields = for_fields
        super().__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):
        if getattr(model_instance, self.attname) is None:
            # no current value
            try:
                # using self.model to retrieve the model class the field belongs to.
                qs = self.model.objects.all()
                if self.for_fields:
                    # filter by objects with the same field values for the fields in "for_fields"
                    # same-as: you filter the QuerySet by the current value of the model fields in for_fields.
                    query = {field: getattr(model_instance, field) for field in self.for_fields}
                    qs = qs.filter(**query)
                # get the order of the last item
                last_item = qs.latest(self.attname)
                value = last_item.order + 1
            except ObjectDoesNotExist:
                value = 0
            # assign the calculated order to the field's value in the model instance using setattr()
            setattr(model_instance, self.attname, value)
            return value
        else:
            return super().pre_save(model_instance, add)


# More info about writing custom model fields at
# https://docs.djangoproject.com/en/3.0/howto/custom-model-fields/