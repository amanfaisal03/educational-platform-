# Project memory

- Before changing student course-player queries or templates, read
  `docs/performance/course-player.md` and run the course-page regression tests.
- Keep course-outline loading scoped to `get_course_for_player`; do not restore
  per-unit/per-lesson lazy queries or load `Material.file_data` while rendering
  the outline. Material content belongs in the dedicated download endpoints.
- Count queries through template rendering, not just through repository calls.
  Include authentication when measuring full HTTP requests.
