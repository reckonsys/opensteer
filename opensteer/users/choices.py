from orm_choices import choices


@choices
class UserRole:
    class Meta:
        ADMIN = [1, 'Admin']  # Create / Delete Permissions
        MANAGER = [2, 'Manager']  # Modify / Report permissions
        REGULAR = [3, 'Regular']  # View permissions
