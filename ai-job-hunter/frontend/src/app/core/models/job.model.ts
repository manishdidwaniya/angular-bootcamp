/** 职位模型 */

export interface Job {
  id: string;
  provider_id: string;
  external_id: string;
  title: string;
  company: string;
  location: string | null;
  work_mode: 'remote' | 'hybrid' | 'onsite' | null;
  salary_min: number | null;
  salary_max: number | null;
  salary_currency: string | null;
  description: string | null;
  url: string;
  company_url: string | null;
  experience_min: number | null;
  experience_max: number | null;
  job_type: 'full-time' | 'part-time' | 'contract' | 'internship' | null;
  posted_at: string | null;
  is_active: boolean;
  skills: JobSkill[];
  created_at: string;
}

export interface JobSkill {
  id: string;
  name: string;
  is_required: boolean;
}

export interface JobMatchResult {
  job: Job;
  score: number;
  explanation: string;
  strengths: string[];
  missing_skills: string[];
  recommendation: 'strong_match' | 'good_match' | 'weak_match' | 'skip';
  suggested_resume_id: string | null;
}

export interface JobSearchFilters {
  query?: string;
  location?: string;
  work_mode?: string;
  salary_min?: number;
  salary_max?: number;
  job_type?: string;
  provider_ids?: string[];
  skills?: string[];
  posted_within_days?: number;
  min_score?: number;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}