import enum


class UserTypes(enum.Enum):
    admin = "Admin"
    user = "User"


class CoachType(enum.Enum):
    boxing = "Boxing Coach"
    swimming = "Swim Coach"
    fitness = "Fitness Coach"


class SportType(enum.Enum):
    boxing = "Boxing"
    swimming = "Swimming"
    fitness = "Fitness"
