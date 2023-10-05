import operator
from functools import reduce

from django.forms import all_valid
from django.views.generic.edit import ModelFormMixin


class InlineFormsetMixin(ModelFormMixin):
    """A model form mixin that handles inline formsets."""

    formset_classes = ()

    def get_formset_kwargs(self):
        """Hook to add additional keyword arguments for the formsets."""
        request = self.request  # noqa
        if request.method in ("POST", "PUT"):
            return {"data": request.POST, "files": request.FILES}
        else:
            return {}

    def get_formset_classes(self):
        """Return a list of formset classes."""
        return self.formset_classes

    def get_formsets(self, parent_instance):
        """Return a list of formset instances."""
        formsets = []
        kwargs = self.get_formset_kwargs()
        kwargs["instance"] = parent_instance
        for formset_class in self.get_formset_classes():
            formsets.append(formset_class(**kwargs))
        return formsets

    def get_context_data(self, formsets=None, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["formsets"] = formsets or self.get_formsets(parent_instance=ctx["form"].instance)
        ctx["combined_media"] = ctx["form"].media
        if ctx["formsets"]:
            ctx["combined_media"] += reduce(operator.add, (fs.media for fs in ctx["formsets"]))
        return ctx

    def formsets_valid(self, formsets):
        """Hook to perform additional actions on the valid formsets."""
        [formset.save() for formset in formsets]

    def form_valid(self, form):
        formsets = self.get_formsets(form.instance)
        if all_valid(formsets):
            response = super().form_valid(form)  # save the form
            self.formsets_valid(formsets)  # save the formsets
            return response
        else:
            return self.form_invalid(form)

    def form_invalid(self, form):
        formsets = self.get_formsets(form.instance)
        [formset.full_clean() for formset in formsets]  # generate formset.errors
        return super().form_invalid(form)
