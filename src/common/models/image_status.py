from enum import Enum


class ImageStatus(Enum):
    """
    The goal of this class represents the status of each screenshot.
    """
    INITIATED = "INITIATED"
    DELETED = "DELETED"
    CROPPED = "CROPPED"
    DREW = "DREW"
