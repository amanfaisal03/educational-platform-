"""Backward-compatible names for the user repository."""

from repositories.user_repository import UserRepository


AuthRepository = UserRepository
AuthorRepository = UserRepository

__all__ = ["AuthRepository", "AuthorRepository"]
