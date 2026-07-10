import { Component, OnInit, inject, signal } from "@angular/core";
import { FormBuilder, ReactiveFormsModule } from "@angular/forms";

import { Profile } from "@core/models/profile.model";
import { ApiService } from "@core/services/api.service";

@Component({
  selector: "ajh-profile",
  standalone: true,
  imports: [ReactiveFormsModule],
  template: `
    <div class="max-w-4xl">
      <p class="text-xs uppercase tracking-widest text-brand-300 font-semibold">
        Matching foundation
      </p>
      <h1 class="text-3xl font-bold mt-2">Career profile</h1>
      <p class="text-[var(--text-muted)] mt-2">
        Accurate recommendations depend on these details. Use commas for
        multiple values.
      </p>

      <form
        [formGroup]="form"
        (ngSubmit)="save()"
        class="grid md:grid-cols-2 gap-5 mt-8"
      >
        <label class="text-sm"
          >Headline
          <input
            formControlName="headline"
            class="field"
            placeholder="Senior Product Manager"
          />
        </label>
        <label class="text-sm"
          >Location
          <input
            formControlName="location"
            class="field"
            placeholder="Bengaluru, India"
          />
        </label>
        <label class="text-sm"
          >Preferred work mode
          <select formControlName="work_mode_preference" class="field">
            <option value="">Any</option>
            <option value="remote">Remote</option>
            <option value="hybrid">Hybrid</option>
            <option value="onsite">On-site</option>
          </select>
        </label>
        <label class="text-sm"
          >Years of experience
          <input
            type="number"
            min="0"
            step="0.5"
            formControlName="experience_years"
            class="field"
          />
        </label>
        <label class="text-sm"
          >Minimum salary
          <input
            type="number"
            min="0"
            formControlName="min_salary"
            class="field"
          />
        </label>
        <label class="text-sm"
          >Salary currency
          <input
            formControlName="salary_currency"
            class="field"
            placeholder="INR"
          />
        </label>
        <label class="text-sm md:col-span-2"
          >Target roles
          <input
            formControlName="roles"
            class="field"
            placeholder="Angular Developer, Full-stack Engineer"
          />
        </label>
        <label class="text-sm md:col-span-2"
          >Skills
          <input
            formControlName="skills"
            class="field"
            placeholder="Angular, TypeScript, Python, FastAPI"
          />
        </label>
        <label class="text-sm"
          >Preferred companies
          <input
            formControlName="preferred_companies"
            class="field"
            placeholder="OpenAI, Microsoft"
          />
        </label>
        <label class="text-sm"
          >Ignored companies
          <input
            formControlName="ignored_companies"
            class="field"
            placeholder="Companies you do not want"
          />
        </label>
        <label class="text-sm md:col-span-2"
          >Professional summary
          <textarea
            rows="5"
            formControlName="summary"
            class="field"
            placeholder="Describe your experience and goals"
          ></textarea>
        </label>
        <div class="md:col-span-2 flex items-center gap-4">
          <button
            type="submit"
            [disabled]="saving()"
            class="rounded-lg bg-brand-300 text-surface-900 font-semibold px-5 py-2.5 disabled:opacity-50"
          >
            {{ saving() ? "Saving..." : "Save profile" }}
          </button>
          @if (message()) {
            <span class="text-sm text-brand-300">{{ message() }}</span>
          }
          @if (error()) {
            <span class="text-sm text-red-400">{{ error() }}</span>
          }
        </div>
      </form>
    </div>
  `,
  styles: [
    `
      .field {
        display: block;
        width: 100%;
        margin-top: 0.4rem;
        padding: 0.7rem 0.85rem;
        border-radius: 0.6rem;
        border: 1px solid var(--border-color);
        background: var(--surface-card);
        color: white;
      }
    `,
  ],
})
export class ProfileComponent implements OnInit {
  private readonly fb = inject(FormBuilder);
  private readonly api = inject(ApiService);
  private existing = false;
  readonly saving = signal(false);
  readonly message = signal<string | null>(null);
  readonly error = signal<string | null>(null);
  readonly form = this.fb.nonNullable.group({
    headline: "",
    summary: "",
    location: "",
    work_mode_preference: "",
    experience_years: 0,
    min_salary: 0,
    salary_currency: "INR",
    roles: "",
    skills: "",
    preferred_companies: "",
    ignored_companies: "",
  });

  ngOnInit(): void {
    this.api.get<Profile>("/profiles/me").subscribe({
      next: (profile) => {
        this.existing = true;
        this.form.patchValue({
          headline: profile.headline ?? "",
          summary: profile.summary ?? "",
          location: profile.location ?? "",
          work_mode_preference: profile.work_mode_preference ?? "",
          experience_years: profile.experience_years,
          min_salary: profile.min_salary ?? 0,
          salary_currency: profile.salary_currency,
          roles: profile.target_roles.map((role) => role.role_title).join(", "),
          skills: profile.skills.map((skill) => skill.name).join(", "),
          preferred_companies: profile.preferred_companies.join(", "),
          ignored_companies: profile.ignored_companies.join(", "),
        });
      },
      error: (err) => {
        if (err.status !== 404) this.error.set("Unable to load your profile.");
      },
    });
  }

  save(): void {
    this.saving.set(true);
    this.error.set(null);
    this.message.set(null);
    const value = this.form.getRawValue();
    const payload = {
      headline: value.headline || null,
      summary: value.summary || null,
      location: value.location || null,
      work_mode_preference: value.work_mode_preference || null,
      experience_years: value.experience_years,
      min_salary: value.min_salary || null,
      salary_currency: value.salary_currency || "INR",
      preferred_companies: this.csv(value.preferred_companies),
      ignored_companies: this.csv(value.ignored_companies),
      skills: this.csv(value.skills).map((name) => ({
        name,
        proficiency_level: "intermediate",
        years_of_experience: 0,
      })),
      target_roles: this.csv(value.roles).map((role_title, index) => ({
        role_title,
        priority: index + 1,
        is_active: true,
      })),
    };
    const request = this.existing
      ? this.api.put<Profile>("/profiles/me", payload)
      : this.api.post<Profile>("/profiles", payload);
    request.subscribe({
      next: () => {
        this.existing = true;
        this.saving.set(false);
        this.message.set("Profile saved.");
      },
      error: (err) => {
        this.saving.set(false);
        this.error.set(err.error?.error?.message ?? "Unable to save profile.");
      },
    });
  }

  private csv(value: string): string[] {
    return [
      ...new Set(
        value
          .split(",")
          .map((item) => item.trim())
          .filter(Boolean),
      ),
    ];
  }
}
