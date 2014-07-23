from django.contrib.admin import SimpleListFilter

class BooleanFilter(SimpleListFilter):
    """
    Two-state filter for boolean fields.

    Simply subclass BooleanFilter and edit the `states` variable to customize the states labels. It is generally not
    useful to change the `value` key of each state.
    `parameter_name` must be the name of the model attribute to filter on.
    """
    title = 'boolean field'
    parameter_name = 'boolean_field'

    states = {
        'on': {
            'value': 'on',
            'label': 'On'
        },

        'off': {
            'value': 'off',
            'label': 'Off'
        }
    }

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return [(self.states['on']['value'], self.states['on']['label']),
                (self.states['off']['value'], self.states['off']['label'])]

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Find all products with identifier ending with the requested version
        if self.value():
            query = {self.parameter_name: self.value() == self.states['on']['value']}
            return queryset.filter(**query)

        else:
            return None
