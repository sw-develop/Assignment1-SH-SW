from rest_framework.pagination import CursorPagination


class AssignCursorPagination(CursorPagination):
    ordering = '-id'