from enum import Enum, auto


class Silhouette(Enum):
    """
    Canonical monster body plans.
    Defines form and posture ONLY.
    """

    BIPEDAL_STRIKER = auto()
    BIPEDAL_HEAVY = auto()

    AVIAN_PROUD = auto()
    AVIAN_DYNAMIC = auto()

    AMPHIB_CRUSTACEAN = auto()
    AMPHIB_CEPHAL = auto()

    QUADRUPED_BESTIAL = auto()
    QUADRUPED_STALKER = auto()

    HOVER_MEDITATIVE = auto()
    HOVER_WEIGHTLESS = auto()
