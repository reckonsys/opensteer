from orm_choices import choices


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


@choices
class DayOfWeek:

    @classmethod
    def next(cls, day):
        if day == cls.SATURDAY:
            return cls.SUNDAY
        return day + 1

    @classmethod
    def previous(cls, day):
        if day == cls.SUNDAY:
            return cls.SATURDAY
        return day - 1

    class Meta:
        SUNDAY = [0, 'Sunday']
        MONDAY = [1, 'Monday']
        TUESDAY = [2, 'Tuesday']
        WEDNESDAY = [3, 'Wednesday']
        THURSDAY = [4, 'Thursday']
        FRIDAY = [5, 'Friday']
        SATURDAY = [6, 'Saturday']
