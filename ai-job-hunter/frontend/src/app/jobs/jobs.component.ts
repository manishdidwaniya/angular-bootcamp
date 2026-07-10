import { Component, OnInit, inject, signal } from "@angular/core";
import { FormBuilder, ReactiveFormsModule } from "@angular/forms";
import { RouterLink } from "@angular/router";

import { Job, JobMatchResult, PaginatedResponse } from "@core/models/job.model";
import { ApiService } from "@core/services/api.service";

interface JobCard {
  job: Job;
  match: JobMatchResult | null;
}

interface PortalSearch {
  name: string;
  note: string;
  url: (query: string, location: string, days: number) => string;
}

@Component({
  selector: "ajh-jobs",
  standalone: true,
  imports: [ReactiveFormsModule, RouterLink],
  template: `
    <div class="flex flex-wrap items-start justify-between gap-4">
      <div>
        <p
          class="text-xs uppercase tracking-widest text-brand-300 font-semibold"
        >
          Freshness enforced
        </p>
        <h1 class="text-3xl font-bold mt-2">Latest jobs</h1>
        <p class="text-[var(--text-muted)] mt-2">
          Only dated, active jobs inside your selected freshness window are
          shown.
        </p>
      </div>
      <button
        (click)="sync()"
        [disabled]="syncing()"
        class="rounded-lg bg-brand-300 text-surface-900 px-4 py-2.5 font-semibold disabled:opacity-50"
      >
        <i class="fa-solid fa-rotate mr-2"></i
        >{{ syncing() ? "Syncing live sources..." : "Sync latest jobs" }}
      </button>
    </div>

    <form
      [formGroup]="filters"
      (ngSubmit)="load()"
      class="grid md:grid-cols-5 gap-3 mt-7 rounded-xl border border-[var(--border-color)] bg-surface-800 p-4"
    >
      <input
        formControlName="query"
        placeholder="Role, skill or company"
        class="field md:col-span-2"
      />
      <input formControlName="location" placeholder="Location" class="field" />
      <select formControlName="freshness" class="field">
        <option [value]="1">Last 24 hours</option>
        <option [value]="3">Last 3 days</option>
        <option [value]="7">Last 7 days</option>
        <option [value]="14">Last 14 days</option>
      </select>
      <button
        type="submit"
        class="rounded-lg border border-brand-300 text-brand-300 px-4 py-2"
      >
        Search
      </button>
    </form>

    <div class="flex gap-2 mt-5">
      <button
        (click)="setMode('latest')"
        [class.bg-brand-300]="mode() === 'latest'"
        [class.text-surface-900]="mode() === 'latest'"
        class="rounded-lg px-4 py-2 border border-[var(--border-color)]"
      >
        Newest first
      </button>
      <button
        (click)="setMode('recommended')"
        [class.bg-brand-300]="mode() === 'recommended'"
        [class.text-surface-900]="mode() === 'recommended'"
        class="rounded-lg px-4 py-2 border border-[var(--border-color)]"
      >
        Best matches
      </button>
      <span class="ml-auto text-sm text-[var(--text-muted)] self-center"
        >{{ total() }} current jobs</span
      >
    </div>

    <section
      class="mt-6 rounded-xl border border-[var(--border-color)] bg-surface-800 p-5"
    >
      <div class="flex flex-wrap items-start justify-between gap-3">
        <div>
          <h2 class="font-semibold text-lg">Search more job portals</h2>
          <p class="text-sm text-[var(--text-muted)] mt-1">
            Opens the same role, location, and freshness search on each official
            portal. Sign-in may be required by the portal.
          </p>
        </div>
        <span class="text-xs text-[var(--text-muted)]"
          >External results are not silently imported</span
        >
      </div>
      <div class="flex flex-wrap gap-2 mt-4">
        @for (portal of portalSearches; track portal.name) {
          <a
            [href]="portalUrl(portal)"
            target="_blank"
            rel="noopener noreferrer"
            [attr.title]="portal.note"
            class="rounded-lg border border-[var(--border-color)] px-3 py-2 text-sm hover:border-brand-300 hover:text-brand-300 transition-colors"
          >
            {{ portal.name }}
            <i class="fa-solid fa-arrow-up-right-from-square ml-1 text-xs"></i>
          </a>
        }
      </div>
    </section>

    @if (syncMessage()) {
      <p class="mt-4 text-sm text-brand-300">{{ syncMessage() }}</p>
    }
    @if (needsProfile()) {
      <section
        class="mt-6 rounded-xl border border-amber-300/40 bg-amber-300/10 p-6"
        role="alert"
      >
        <div class="flex gap-4 items-start">
          <i class="fa-solid fa-user-pen text-amber-300 text-xl mt-1"></i>
          <div>
            <h2 class="font-semibold text-lg">Complete your career profile</h2>
            <p class="text-sm text-[var(--text-muted)] mt-2">
              Best Matches needs your target roles, skills, experience, and
              preferences before it can rank jobs accurately.
            </p>
            <div class="flex flex-wrap gap-3 mt-4">
              <a
                routerLink="/profiles"
                class="rounded-lg bg-brand-300 text-surface-900 px-4 py-2 text-sm font-semibold"
                >Create profile</a
              >
              <button
                type="button"
                (click)="setMode('latest')"
                class="rounded-lg border border-[var(--border-color)] px-4 py-2 text-sm"
              >
                Browse newest jobs instead
              </button>
            </div>
          </div>
        </div>
      </section>
    } @else if (error()) {
      <section
        class="mt-6 rounded-xl border border-red-400/40 bg-red-400/10 p-4 text-sm text-red-300"
        role="alert"
      >
        <i class="fa-solid fa-circle-exclamation mr-2"></i>{{ error() }}
      </section>
    }
    @if (loading()) {
      <div class="py-16 text-center text-[var(--text-muted)]">
        <i class="fa-solid fa-spinner fa-spin mr-2"></i>Loading accurate jobs...
      </div>
    }

    @if (!loading() && !needsProfile() && !error()) {
      <div class="grid gap-4 mt-6">
        @for (card of cards(); track card.job.id) {
          <article
            class="rounded-xl border border-[var(--border-color)] bg-surface-800 p-5 hover:border-brand-300 transition-colors"
          >
            <div class="flex flex-wrap gap-4 justify-between">
              <div class="min-w-0">
                <div class="flex flex-wrap gap-2 items-center">
                  <span
                    class="text-xs rounded-full bg-brand-300/15 text-brand-300 px-2.5 py-1"
                    >{{ age(card.job) }}</span
                  ><span class="text-xs text-[var(--text-muted)]">{{
                    card.job.source
                  }}</span>
                  @if (card.match) {
                    <span
                      class="text-xs rounded-full bg-sky-400/15 text-sky-300 px-2.5 py-1"
                      >{{ card.match.score }}% match</span
                    >
                  }
                </div>
                <h2 class="font-semibold text-xl mt-3">{{ card.job.title }}</h2>
                <p class="text-brand-300 mt-1">{{ card.job.company }}</p>
                <p class="text-sm text-[var(--text-muted)] mt-2">
                  {{ card.job.location || "Location not specified" }} ·
                  {{ card.job.work_mode || "Work mode not specified" }}
                </p>
              </div>
              <div class="flex gap-2 items-start">
                <button
                  (click)="track(card.job)"
                  class="rounded-lg border border-[var(--border-color)] px-3 py-2 text-sm"
                >
                  Track</button
                ><a
                  [href]="card.job.url"
                  target="_blank"
                  rel="noopener"
                  class="rounded-lg bg-brand-300 text-surface-900 px-3 py-2 text-sm font-semibold"
                  >Apply
                  <i class="fa-solid fa-arrow-up-right-from-square ml-1"></i
                ></a>
              </div>
            </div>
            @if (card.job.skills.length) {
              <div class="flex flex-wrap gap-2 mt-4">
                @for (skill of card.job.skills.slice(0, 8); track skill.id) {
                  <span
                    class="text-xs rounded bg-surface-900 px-2 py-1 text-[var(--text-muted)]"
                    >{{ skill.name }}</span
                  >
                }
              </div>
            }
            @if (card.match) {
              <p class="text-sm text-[var(--text-muted)] mt-4">
                {{ card.match.explanation }}
              </p>
            }
          </article>
        } @empty {
          <div
            class="rounded-xl border border-[var(--border-color)] bg-surface-800 p-8 text-center text-[var(--text-muted)]"
          >
            No fresh jobs match these filters. Try a wider freshness window or
            sync the providers.
          </div>
        }
      </div>
    }
  `,
  styles: [
    `
      .field {
        width: 100%;
        border-radius: 0.55rem;
        border: 1px solid var(--border-color);
        background: var(--surface-bg);
        color: white;
        padding: 0.65rem 0.75rem;
      }
    `,
  ],
})
export class JobsComponent implements OnInit {
  private readonly api = inject(ApiService);
  private readonly fb = inject(FormBuilder);
  readonly filters = this.fb.nonNullable.group({
    query: "",
    location: "",
    freshness: 7,
  });
  readonly cards = signal<JobCard[]>([]);
  readonly total = signal(0);
  readonly loading = signal(false);
  readonly syncing = signal(false);
  readonly error = signal<string | null>(null);
  readonly needsProfile = signal(false);
  readonly syncMessage = signal<string | null>(null);
  readonly mode = signal<"latest" | "recommended">("recommended");
  readonly portalSearches: PortalSearch[] = [
    {
      name: "Y Combinator",
      note: "Search startup roles on Y Combinator Work at a Startup.",
      url: (query) =>
        `https://www.ycombinator.com/jobs?query=${encodeURIComponent(query)}`,
    },
    {
      name: "ZipRecruiter",
      note: "Search current jobs directly on ZipRecruiter.",
      url: (query, location, days) =>
        `https://www.ziprecruiter.com/jobs-search?search=${encodeURIComponent(query)}&location=${encodeURIComponent(location)}&days=${days}`,
    },
    {
      name: "Cutshort",
      note: "Search technology jobs directly on Cutshort.",
      url: (query) =>
        `https://cutshort.io/jobs?search=${encodeURIComponent(query)}`,
    },
    {
      name: "LinkedIn",
      note: "Search LinkedIn Jobs posted during the selected window.",
      url: (query, location, days) =>
        `https://www.linkedin.com/jobs/search/?keywords=${encodeURIComponent(query)}&location=${encodeURIComponent(location)}&f_TPR=r${days * 86400}`,
    },
    {
      name: "Instahyre",
      note: "Search curated technology roles directly on Instahyre.",
      url: (query) =>
        `https://www.instahyre.com/search-jobs/?search=${encodeURIComponent(query)}`,
    },
    {
      name: "Glassdoor",
      note: "Search jobs directly on Glassdoor.",
      url: (query, location, days) =>
        `https://www.glassdoor.com/Job/jobs.htm?sc.keyword=${encodeURIComponent(query)}&locKeyword=${encodeURIComponent(location)}&fromAge=${days}`,
    },
    {
      name: "Naukri",
      note: "Search current India-focused jobs directly on Naukri.",
      url: (query, location, days) =>
        `https://www.naukri.com/jobs-in-${encodeURIComponent(location.toLowerCase().replace(/\s+/g, "-"))}?k=${encodeURIComponent(query)}&jobAge=${days}`,
    },
    {
      name: "Google Jobs",
      note: "Search recent jobs across the web with Google.",
      url: (query, location, days) => {
        const period = days <= 1 ? "d" : days <= 7 ? "w" : "m";
        return `https://www.google.com/search?q=${encodeURIComponent(`${query} jobs ${location}`)}&tbs=qdr:${period}`;
      },
    },
  ];

  ngOnInit(): void {
    this.load();
  }

  setMode(mode: "latest" | "recommended"): void {
    this.mode.set(mode);
    this.load();
  }

  load(): void {
    this.loading.set(true);
    this.error.set(null);
    this.needsProfile.set(false);
    const value = this.filters.getRawValue();
    const path = this.mode() === "recommended" ? "/jobs/recommended" : "/jobs";
    const params = {
      query: value.query || undefined,
      location: value.location || undefined,
      posted_within_days: value.freshness,
      page_size: 50,
    };
    if (this.mode() === "recommended") {
      this.api.get<PaginatedResponse<JobMatchResult>>(path, params).subscribe({
        next: (response) => {
          this.cards.set(
            response.items.map((match) => ({ job: match.job, match })),
          );
          this.total.set(response.total);
          this.loading.set(false);
        },
        error: (err) => {
          this.loading.set(false);
          this.cards.set([]);
          this.total.set(0);
          const message = this.errorMessage(
            err,
            "Unable to calculate recommendations right now.",
          );
          if (err.status === 422 && message.toLowerCase().includes("profile")) {
            this.needsProfile.set(true);
          } else {
            this.error.set(message);
          }
        },
      });
    } else {
      this.api.get<PaginatedResponse<Job>>(path, params).subscribe({
        next: (response) => {
          this.cards.set(response.items.map((job) => ({ job, match: null })));
          this.total.set(response.total);
          this.loading.set(false);
        },
        error: (err) => {
          this.loading.set(false);
          this.cards.set([]);
          this.total.set(0);
          this.error.set(
            this.errorMessage(err, "Unable to load jobs right now."),
          );
        },
      });
    }
  }

  sync(): void {
    this.syncing.set(true);
    this.syncMessage.set(null);
    this.error.set(null);
    this.needsProfile.set(false);
    const value = this.filters.getRawValue();
    this.api
      .post<{ created: number; accepted: number }>("/providers/sync", {
        terms: value.query ? [value.query] : [],
        locations: value.location ? [value.location] : [],
        freshness_days: value.freshness,
      })
      .subscribe({
        next: (response) => {
          this.syncing.set(false);
          this.syncMessage.set(
            `Live sync complete: ${response.created} new and ${response.accepted} verified current jobs.`,
          );
          this.load();
        },
        error: (err) => {
          this.syncing.set(false);
          this.error.set(
            this.errorMessage(err, "Live sync failed. Check provider status."),
          );
        },
      });
  }

  track(job: Job): void {
    this.api.post("/applications", { job_id: job.id }).subscribe({
      next: () =>
        this.syncMessage.set(`Tracking ${job.title} at ${job.company}.`),
      error: (err) =>
        this.error.set(
          this.errorMessage(err, "Unable to track this application."),
        ),
    });
  }

  age(job: Job): string {
    const hours = Math.max(0, Math.round(job.age_hours));
    return hours < 24 ? `${hours}h ago` : `${Math.floor(hours / 24)}d ago`;
  }

  portalUrl(portal: PortalSearch): string {
    const values = this.filters.getRawValue();
    return portal.url(
      values.query.trim() || "Software Developer",
      values.location.trim() || "Remote",
      values.freshness,
    );
  }

  private errorMessage(error: unknown, fallback: string): string {
    if (typeof error !== "object" || error === null) return fallback;
    const response = error as {
      error?: {
        error?: { message?: string };
        detail?: string;
        message?: string;
      };
    };
    return (
      response.error?.error?.message ??
      response.error?.detail ??
      response.error?.message ??
      fallback
    );
  }
}
