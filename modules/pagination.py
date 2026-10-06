
class pagination(object):
    def calculate_pagination(
        total: int,
        page: int,
        per_page: int,
    ) -> tuple[int, int, int]:
        if per_page < 1:
            raise ValueError("per_page must be at least 1")

        total_pages = max((total + per_page - 1) // per_page, 1)
        page = max(1, min(page, total_pages))
        offset = (page - 1) * per_page

        return page, total_pages, offset


__all__=["pagination"]