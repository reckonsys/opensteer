from orm_choices import choices


@choices
class DayOfWeek:

    @classmethod
    def edge_days(cls):
        first_day, _ = cls.CHOICES[0]
        last_day, _ = cls.CHOICES[-1]
        return first_day, last_day

    @classmethod
    def next(cls, day):
        first_day, last_day = cls.edge_days()
        if day == last_day:
            return first_day
        return day + 1

    @classmethod
    def previous(cls, day):
        first_day, last_day = cls.edge_days()
        if day == first_day:
            return last_day
        return day - 1

    class Meta:
        MONDAY = [0, 'Monday']
        TUESDAY = [1, 'Tuesday']
        WEDNESDAY = [2, 'Wednesday']
        THURSDAY = [3, 'Thursday']
        FRIDAY = [4, 'Friday']
        SATURDAY = [5, 'Saturday']
        SUNDAY = [6, 'Sunday']


@choices
class QuestionKind:
    class Meta:
        TEXT = [1, 'Text']
        NUMERIC = [2, 'Numeric']
        BOOLEAN = [3, 'Boolean']
        CHOICE = [4, 'Choice']
        MULTIPLE_CHOICE = [5, 'Multiple Choice']


@choices
class QuestionCategory:
    class Meta:
        STANDUP = [1, 'Standup']
        CHECKIN = [2, 'Checkin']
