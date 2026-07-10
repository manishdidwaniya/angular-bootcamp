/** 档案模型 — 不硬编码任何特定职业 */

export interface Skill {
  id: string;
  name: string;
  category: string | null;
  proficiency_level: string;
  years_of_experience: number;
}

export interface TargetRole {
  id: string;
  role_title: string;
  priority: number;
  is_active: boolean;
}

export interface Profile {
  id: string;
  headline: string | null;
  summary: string | null;
  location: string | null;
  work_mode_preference: 'remote' | 'hybrid' | 'onsite' | null;
  min_salary: number | null;
  max_salary: number | null;
  salary_currency: string;
  experience_years: number;
  notice_period_days: number | null;
  preferred_companies: string[];
  ignored_companies: string[];
  certifications: string[];
  languages: string[];
  skills: Skill[];
  target_roles: TargetRole[];
  created_at: string;
}

export interface ProfileCreateRequest {
  headline?: string;
  summary?: string;
  location?: string;
  work_mode_preference?: string;
  min_salary?: number;
  max_salary?: number;
  salary_currency?: string;
  experience_years?: number;
  notice_period_days?: number;
  preferred_companies?: string[];
  ignored_companies?: string[];
  certifications?: string[];
  languages?: string[];
  skills?: SkillInput[];
  target_roles?: TargetRoleInput[];
}

export interface SkillInput {
  name: string;
  proficiency_level?: string;
  years_of_experience?: number;
}

export interface TargetRoleInput {
  role_title: string;
  priority?: number;
  is_active?: boolean;
}