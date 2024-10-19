import math

from google.cloud.vision_v1 import EntityAnnotation

from src.common.models.object_boundary import ObjectBoundary


class TextAnnotation:
    """
    This hold customized interface for Google OCR annotation
    """

    description: str
    boundary: ObjectBoundary

    def __init__(self, description: str, boundary: ObjectBoundary):
        self.description = description
        self.boundary = boundary

    @classmethod
    def build_annotation_from_google_annotation(cls, google_annotation: EntityAnnotation):
        annotation_vertices = google_annotation.bounding_poly.vertices
        x_min = annotation_vertices[0].x
        x_max = annotation_vertices[0].x
        y_min = annotation_vertices[1].y
        y_max = annotation_vertices[1].y
        for vertex in annotation_vertices:
            x_min = min(x_min, vertex.x)
            x_max = max(x_max, vertex.x)
            y_min = min(y_min, vertex.y)
            y_max = max(y_max, vertex.y)

        boundary = ObjectBoundary(x_min, y_min, x_max, y_max)
        return cls(
            google_annotation.description,
            boundary
        )
