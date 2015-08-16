class OccurrenceReplacer(object):
    """
    Replace missing occurrences in a date rage.

    When getting a list of occurrences, the last thing that needs to be done
    before passing it forward is to make sure all of the occurrences that
    have been stored in the datebase replace, in the list you are returning,
    the generated ones that are equivalent. This class makes this easier.
    """

    def __init__(self, persisted_occurrences):
        lookup = [
            ((occurrence.event, occurrence.original_start, occurrence.original_end), occurrence) for
            occurrence in persisted_occurrences]
        self.lookup = dict(lookup)

    def get_occurrence(self, occurrence):
        """
        Return a persisted occurrences matching the occurrence

        Returned occurrence will be removed from future lookup as it's been matched
        """
        return self.lookup.pop(
            (occurrence.event, occurrence.original_start, occurrence.original_end),
            occurrence)

    def has_occurrence(self, occurrence):
        return (occurrence.event, occurrence.original_start, occurrence.original_end) in self.lookup

    def get_additional_occurrences(self, start, end):
        """Return persisted occurrences which are now in the period"""
        occurrences = []
        for key, occurrence in self.lookup.items():
            if (end and occurrence.start < end) and occurrence.end >= start and not occurrence.cancelled:
                occurrences.append(occurrence)
        return occurrences
