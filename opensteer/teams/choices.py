from orm_choices import choices


@choices
class MembershipRole:
    class Meta:
        REGULAR = [1, 'Regular']
        MANAGER = [2, 'Manager']
