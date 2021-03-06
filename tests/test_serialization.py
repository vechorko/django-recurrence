from datetime import datetime
from recurrence import Recurrence, Rule
import recurrence


def test_rule_serialization():
    rule = Rule(
        recurrence.WEEKLY
    )

    serialized = recurrence.serialize(rule)
    assert 'RRULE:FREQ=WEEKLY' == serialized
    assert recurrence.deserialize(serialized) == Recurrence(rrules=[rule])


def test_complex_rule_serialization():
    rule = Rule(
        recurrence.WEEKLY,
        interval=17,
        wkst=1,
        count=7,
        byday=[
            recurrence.to_weekday('-1MO'),
            recurrence.to_weekday('TU')
        ],
        bymonth=[1, 3]
    )

    serialized = recurrence.serialize(rule)
    assert ('RRULE:FREQ=WEEKLY;INTERVAL=17;WKST=TU;'
            'COUNT=7;BYDAY=-1MO,TU;BYMONTH=1,3') == serialized
    assert recurrence.deserialize(serialized) == Recurrence(rrules=[rule])


def test_bug_in_count_and_until_rule_serialization():
    # This tests a bug in the way we serialize rules with instance
    # counts and an until date. We should really raise a
    # ValidationError in validate if you specify both, but we
    # currently don't. Once we start doing this, this test can be
    # modified to check an exception is raised.
    rule = Rule(
        recurrence.WEEKLY,
        count=7,
        until=datetime(2014, 10, 31, 0, 0, 0)
    )

    serialized = recurrence.serialize(rule)

    # Note that we've got no UNTIL value here
    assert 'RRULE:FREQ=WEEKLY;COUNT=7' == serialized
