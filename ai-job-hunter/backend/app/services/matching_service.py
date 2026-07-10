"""Profile-aware job matching with deterministic, explainable scoring."""

import re
from difflib import SequenceMatcher

from app.models.job import Job
from app.models.profile import Profile
from app.schemas.job import JobMatchResult, JobRead


class MatchingService:
    def score(self, job: Job, profile: Profile, job_read: JobRead) -> JobMatchResult:
        profile_skills = {skill.name.lower() for skill in profile.skills}
        job_skills = {skill.name.lower() for skill in job.skills}
        text = f"{job.title} {job.description or ''}".lower()
        detected_profile_skills = {skill for skill in profile_skills if skill in text}
        matched_skills = job_skills & profile_skills | detected_profile_skills
        missing_skills = sorted(job_skills - profile_skills)

        strengths: list[str] = []
        parts: list[str] = []
        score = 0.0

        role_score = self._role_score(job, profile)
        score += role_score
        if role_score >= 17:
            strengths.append("Target role alignment")
        parts.append(f"role {role_score:.0f}/25")

        if profile_skills:
            denominator = max(len(job_skills or profile_skills), 1)
            skill_score = min(25.0, 25.0 * len(matched_skills) / denominator)
        else:
            skill_score = 0.0
        score += skill_score
        if skill_score >= 15:
            strengths.append(f"{len(matched_skills)} matching skills")
        parts.append(f"skills {skill_score:.0f}/25")

        experience_score = self._experience_score(job, profile.experience_years)
        score += experience_score
        if experience_score >= 8:
            strengths.append("Experience fit")
        parts.append(f"experience {experience_score:.0f}/10")

        salary_score = self._salary_score(job, profile)
        score += salary_score
        if salary_score >= 8:
            strengths.append("Salary fit")
        parts.append(f"salary {salary_score:.0f}/10")

        location_score = self._location_score(job, profile)
        score += location_score
        if location_score >= 8:
            strengths.append("Location fit")
        parts.append(f"location {location_score:.0f}/10")

        work_mode_score = self._work_mode_score(job, profile)
        score += work_mode_score
        if work_mode_score >= 6:
            strengths.append("Work-mode fit")
        parts.append(f"work mode {work_mode_score:.0f}/8")

        company_score = self._company_score(job, profile)
        if company_score < 0:
            score = 0.0
            parts.append("ignored company")
        else:
            score += company_score
            if company_score == 5:
                strengths.append("Preferred company")
            parts.append(f"company {company_score:.0f}/5")

        freshness_score = max(0.0, 7.0 * (1.0 - job_read.age_hours / (7 * 24)))
        score += freshness_score
        if job_read.age_hours <= 48:
            strengths.append("Posted within 48 hours")
        parts.append(f"freshness {freshness_score:.0f}/7")

        resume_id, resume_score = self._best_resume(job, profile)
        if resume_score >= 0.25:
            strengths.append("Resume text alignment")

        score = round(max(0.0, min(score, 100.0)), 1)
        recommendation = (
            "strong_match"
            if score >= 80
            else "good_match" if score >= 65 else "weak_match" if score >= 45 else "skip"
        )
        explanation = f"{score:.1f}% match based on " + ", ".join(parts) + "."
        return JobMatchResult(
            job=job_read,
            score=score,
            explanation=explanation,
            strengths=strengths,
            missing_skills=missing_skills,
            recommendation=recommendation,
            suggested_resume_id=resume_id,
        )

    @staticmethod
    def _similarity(left: str, right: str) -> float:
        return SequenceMatcher(None, left.lower().strip(), right.lower().strip()).ratio()

    def _role_score(self, job: Job, profile: Profile) -> float:
        active_roles = [role for role in profile.target_roles if role.is_active]
        if not active_roles:
            return 0.0
        return 25.0 * max(self._similarity(job.title, role.role_title) for role in active_roles)

    @staticmethod
    def _experience_score(job: Job, years: float) -> float:
        minimum = job.experience_min
        maximum = job.experience_max
        if minimum is None and job.description:
            match = re.search(r"(\d+(?:\.\d+)?)\+?\s*(?:years|yrs)", job.description.lower())
            minimum = float(match.group(1)) if match else None
        if minimum is None and maximum is None:
            return 5.0
        if minimum is not None and years < minimum:
            return max(0.0, 10.0 - (minimum - years) * 3)
        if maximum is not None and years > maximum + 5:
            return 7.0
        return 10.0

    @staticmethod
    def _salary_score(job: Job, profile: Profile) -> float:
        if profile.min_salary is None:
            return 5.0
        if job.salary_max is None and job.salary_min is None:
            return 4.0
        offered = job.salary_max or job.salary_min or 0
        return (
            10.0 if offered >= profile.min_salary else max(0.0, 10.0 * offered / profile.min_salary)
        )

    @staticmethod
    def _location_score(job: Job, profile: Profile) -> float:
        if not profile.location:
            return 5.0
        if job.work_mode == "remote":
            return 10.0
        location = (job.location or "").lower()
        return 10.0 if profile.location.lower() in location else 2.0

    @staticmethod
    def _work_mode_score(job: Job, profile: Profile) -> float:
        if not profile.work_mode_preference:
            return 4.0
        return 8.0 if job.work_mode == profile.work_mode_preference else 1.0

    @staticmethod
    def _company_score(job: Job, profile: Profile) -> float:
        company = job.company.lower()
        if any(name.lower() in company for name in profile.ignored_companies):
            return -100.0
        if any(name.lower() in company for name in profile.preferred_companies):
            return 5.0
        return 2.0

    def _best_resume(self, job: Job, profile: Profile) -> tuple[str | None, float]:
        text = f"{job.title} {job.description or ''}"
        candidates = [
            resume for resume in profile.resumes if resume.is_active and resume.parsed_content
        ]
        if not candidates:
            return None, 0.0
        best = max(
            candidates, key=lambda resume: self._similarity(text, resume.parsed_content or "")
        )
        return str(best.id), self._similarity(text, best.parsed_content or "")
