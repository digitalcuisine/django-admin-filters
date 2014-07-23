from django.contrib.admin import SimpleListFilter


class GenericFieldFilter(SimpleListFilter):
    """
    Provide a filter for any model field. Might be costly on large tables.
    
    The `lookups` method will gather all existing values for the field and build up the filter's list from them.
    It is possible to customize the label used for each possible value by overriding the `value_label` method.
    """
    
    title = 'field'
    parameter_name = 'field'

    # Use the raw value as label by default
    @staticmethod
    def value_label(value):
        return value

    def filter_values(self, model_admin):
        """
        Returns a list of possible values for the filter.
        By default, all existing values for the filtered attribute are loaded and made into a 
        unique list.
        As this might be quite costly, you can override this method to provide your own list of
        values
        """
        values = model_admin.model.objects.all().values_list(self.parameter_name, flat=True)
        #  Unique values list (see f6 in http://www.peterbe.com/plog/uniqifiers-benchmark)
        return list(set(values))

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        
        # Get values and labels, and sort by label
        values = self.filter_values(model_admin)
        filters = sorted([(self.value_label(value), value) for value in values])

        return (
            (value, label) for label, value in filters
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Find all products with identifier ending with the requested version
        if self.value():
            query = {self.parameter_name: self.value()}
            return queryset.filter(**query)
        else:
            return None
