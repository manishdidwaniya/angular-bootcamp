"""导出所有 ORM 模型，确保 Alembic 能发现它们。"""

from app.models.application import Application
from app.models.job import Job, job_skills_table
from app.models.notification import Notification
from app.models.profile import Profile, TargetRole, profile_skills_table
from app.models.provider import Provider
from app.models.resume import Resume
from app.models.search import Search
from app.models.settings import UserSettings
from app.models.skill import Skill
from app.models.user import User

__all__ = [
    "User",
    "Profile",
    "TargetRole",
    "Skill",
    "Resume",
    "Job",
    "Provider",
    "Application",
    "Notification",
    "Search",
    "UserSettings",
    "job_skills_table",
    "profile_skills_table",
]
