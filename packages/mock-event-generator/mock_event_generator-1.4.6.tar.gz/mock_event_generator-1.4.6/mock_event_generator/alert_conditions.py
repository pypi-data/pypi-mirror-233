"""Utility and setting of the alert conditions.

To be used (in future in gwcelery)
Implement:
- is_significant(event: dict[str, Any]) -> bool
- should_publish(event: dict[str, Any]) -> bool
"""

from typing import Any


class AlertConditions:
    """Class that define the threshould for alerts.

    The value are determined by the ``thresholds`` static dictionary.
    """

    one_day = 1 / 3600 / 24
    one_month = 1 / 3600 / 24 / 30
    one_year = 1 / 3600 / 24 / 365
    thresholds_cbc = 2 * one_day
    thresholds_burst = 2 * one_day
    thresholds: dict[tuple[str, str, str], tuple[float, float]] = {
        # CBC AllSKy searches
        ('cbc', 'mbta', 'allsky'): (2 * one_day, one_month / 6),
        ('cbc', 'gstlal', 'allsky'): (2 * one_day, one_month / 6),
        ('cbc', 'pycbc', 'allsky'): (2 * one_day, one_month / 6),
        ('cbc', 'spiir', 'allsky'): (2 * one_day, one_month / 6),
        # CBC EarlyWarning searches
        ('cbc', 'mbta', 'earlywarning'): (one_month, one_month / 6),
        ('cbc', 'gstlal', 'earlywarning'): (one_month, one_month / 6),
        ('cbc', 'pycbc', 'earlywarning'): (one_month, one_month / 6),
        ('cbc', 'spiir', 'earlywarning'): (one_month, one_month / 6),
        # CBC SSM searches
        ('cbc', 'mbta', 'ssm'): (one_month / 6, one_year / 4),
        ('cbc', 'gstlal', 'ssm'): (one_month / 6, one_year / 4),
        # BURST BBH searches
        ('burst', 'cwb', 'bbh'): (2 * one_day, one_month / 6),
        # BURST AllSky searches
        ('burst', 'cwb', 'allsky'): (2 * one_day, one_year / 4),
        ('burst', 'olib', 'allsky'): (2 * one_day / 6, one_year / 4),
        # CBC MDC gstlal
        ('cbc', 'gstlal', 'mdc'): (2 * one_day, one_month / 6),
    }

    def get_far(self, group: str, pipeline: str, search: str) -> float:
        """Method that return the far threshould for generating alerts.

        Parameters
        ----------
        group : str
        pipeline : str
        search : str

        Returns
        -------
        far : float
        """
        return self.thresholds.get((group, pipeline, search), (0.0, 0.0))[0]

    def get_significant_far(self, group: str, pipeline: str, search: str) -> float:
        """Method that return the far threshould for significant alerts.

        Parameters
        ----------
        group : str
        pipeline : str
        search : str

        Returns
        -------
        far : float
        """
        return self.thresholds.get((group, pipeline, search), (0.0, 0.0))[1]


alert_conditions = AlertConditions()


def is_significant(event: dict[str, Any]) -> bool:
    """Determine whether an event should be considered a significant event.

    All of the following conditions must be true for a public alert:

    *   The event's ``offline`` flag is not set.
    *   The event's is not an injection.
    *   The event's false alarm rate is less than or equal to
        :obj:`~gwcelery.conf.alert_far_thresholds`

    or the event has been marked to generate a RAVEN alert.

    Parameters
    ----------
    event : dict
        Event dictionary (e.g., the return value from
        :meth:`gwcelery.tasks.gracedb.get_event`, or
        ``preferred_event_data`` in igwn-alert packet.)

    Returns
    -------
    _is_significant : bool
        :obj:`True` if the event meets the criteria for a signifincat alert.
        :obj:`False` if it does not.

    """
    ev_group = event.get('group', '').lower()
    ev_pipeline = event.get('pipeline', '').lower()
    ev_search = event.get('search', '').lower()
    ev_far = event.get('far', 0.0)
    far_threshold = alert_conditions.get_significant_far(
        ev_group, ev_pipeline, ev_search
    )
    _is_significant = (
        (not event['offline'])
        and ('INJ' not in event['labels'])
        and (ev_far < far_threshold)
    ) or ('RAVEN_ALERT' in event['labels'])

    return _is_significant


def should_publish(event: dict[str, Any]) -> bool:
    """Determine whether an event should be published as a public alert.

    All of the following conditions must be true for a public alert:

    *   The event's ``offline`` flag is not set.
    *   The event's is not an injection.
    *   The event's false alarm rate is less than or equal to
        :obj:`~gwcelery.conf.alert_far_thresholds`

    or the event has been marked to generate a RAVEN alert.

    Parameters
    ----------
    event : dict
        Event dictionary (e.g., the return value from
        :meth:`gwcelery.tasks.gracedb.get_event`, or
        ``preferred_event_data`` in igwn-alert packet.)

    Returns
    -------
    should_publish : bool
        :obj:`True` if the event meets the criteria for a public alert or
        :obj:`False` if it does not.

    """
    ev_group = event.get('group', '').lower()
    ev_pipeline = event.get('pipeline', '').lower()
    ev_search = event.get('search', '').lower()
    ev_far = event.get('far', 0.0)
    far_threshold = alert_conditions.get_far(ev_group, ev_pipeline, ev_search)
    _should_publish = (
        (not event['offline'])
        and ('INJ' not in event['labels'])
        and (ev_far < far_threshold)
    ) or ('RAVEN_ALERT' in event['labels'])

    return _should_publish
