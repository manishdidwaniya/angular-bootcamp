"""Profile 业务逻辑。"""

from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import ConflictException, NotFoundException
from app.models.profile import Profile, TargetRole, profile_skills_table
from app.models.skill import Skill
from app.repositories.profile_repository import ProfileRepository
from app.schemas.profile import ProfileCreate, ProfileUpdate


class ProfileService:
    """档案服务 — 创建、读取、更新用户档案。"""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = ProfileRepository(db)

    async def create(self, user_id: str, data: ProfileCreate) -> Profile:
        """创建档案，包括技能和目标角色。"""
        existing = await self.repo.find_by_user_id(user_id)
        if existing:
            raise ConflictException("Profile already exists for this user.")

        profile = Profile(
            user_id=user_id,
            headline=data.headline,
            summary=data.summary,
            location=data.location,
            work_mode_preference=data.work_mode_preference,
            min_salary=data.min_salary,
            max_salary=data.max_salary,
            salary_currency=data.salary_currency,
            experience_years=data.experience_years,
            notice_period_days=data.notice_period_days,
            preferred_companies=data.preferred_companies,
            ignored_companies=data.ignored_companies,
            certifications=data.certifications,
            languages=data.languages,
        )
        self.db.add(profile)
        await self.db.flush()

        # 处理技能
        for skill_input in data.skills:
            skill = await self._get_or_create_skill(
                skill_input.name, skill_input.category if hasattr(skill_input, "category") else None
            )
            await self.db.execute(
                profile_skills_table.insert().values(
                    profile_id=profile.id,
                    skill_id=skill.id,
                    proficiency_level=skill_input.proficiency_level,
                    years_of_experience=skill_input.years_of_experience,
                )
            )

        # 处理目标角色
        for role_input in data.target_roles:
            role = TargetRole(
                profile_id=profile.id,
                role_title=role_input.role_title,
                priority=role_input.priority,
                is_active=role_input.is_active,
            )
            self.db.add(role)

        await self.db.flush()
        await self.db.refresh(profile)
        await self.db.refresh(profile, attribute_names=["skills", "target_roles"])
        return profile

    async def get_by_user_id(self, user_id: str) -> Profile:
        """获取用户的档案。"""
        profile = await self.repo.find_by_user_id(user_id)
        if not profile:
            raise NotFoundException("Profile", user_id)
        return profile

    async def update(self, user_id: str, data: ProfileUpdate) -> Profile:
        """更新用户档案。"""
        profile = await self.get_by_user_id(user_id)
        update_data = data.model_dump(exclude_unset=True)
        skills = update_data.pop("skills", None)
        target_roles = update_data.pop("target_roles", None)

        for key, value in update_data.items():
            setattr(profile, key, value)

        if skills is not None:
            await self.db.execute(
                delete(profile_skills_table).where(
                    profile_skills_table.c.profile_id == str(profile.id)
                )
            )
            for skill_data in skills:
                skill = await self._get_or_create_skill(skill_data["name"])
                await self.db.execute(
                    profile_skills_table.insert().values(
                        profile_id=str(profile.id),
                        skill_id=str(skill.id),
                        proficiency_level=skill_data.get("proficiency_level", "intermediate"),
                        years_of_experience=skill_data.get("years_of_experience", 0),
                    )
                )

        if target_roles is not None:
            await self.db.execute(
                delete(TargetRole).where(TargetRole.profile_id == str(profile.id))
            )
            for role_data in target_roles:
                self.db.add(TargetRole(profile_id=str(profile.id), **role_data))

        await self.db.flush()
        await self.db.refresh(profile)
        if skills is not None or target_roles is not None:
            await self.db.refresh(profile, attribute_names=["skills", "target_roles"])
        return profile

    async def _get_or_create_skill(self, name: str, category: str | None = None) -> Skill:
        """获取或创建技能。"""
        from sqlalchemy import select

        query = select(Skill).where(Skill.name == name)
        result = await self.db.execute(query)
        skill = result.scalar_one_or_none()
        if not skill:
            skill = Skill(name=name, category=category)
            self.db.add(skill)
            await self.db.flush()
        return skill
