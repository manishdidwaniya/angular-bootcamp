import { Component, OnInit, inject, signal } from '@angular/core';

import { Job, PaginatedResponse } from '@core/models/job.model';
import { ApiService } from '@core/services/api.service';

@Component({
  selector: 'ajh-jobs',
  standalone: true,
  template: `
    <h1 class="text-3xl font-bold">Jobs</h1>
    <p class="text-[var(--text-muted)] mt-2">Browse jobs collected from configured providers.</p>
    <div class="grid gap-4 mt-8">
      @for (job of jobs(); track job.id) {
        <article class="rounded-xl border border-[var(--border-color)] bg-surface-800 p-5">
          <h2 class="font-semibold text-lg">{{ job.title }}</h2>
          <p class="text-brand-300">{{ job.company }}</p>
          <p class="text-sm text-[var(--text-muted)] mt-2">{{ job.location || 'Location not specified' }} · {{ job.work_mode || 'Flexible' }}</p>
          <a [href]="job.url" target="_blank" rel="noopener" class="inline-block text-sm text-brand-300 mt-4">View job</a>
        </article>
      } @empty {
        <div class="rounded-xl border border-[var(--border-color)] bg-surface-800 p-6 text-[var(--text-muted)]">No jobs have been imported yet.</div>
      }
    </div>
  `,
})
export class JobsComponent implements OnInit {
  private readonly api = inject(ApiService);
  readonly jobs = signal<Job[]>([]);

  ngOnInit(): void {
    this.api.get<PaginatedResponse<Job>>('/jobs').subscribe(response => this.jobs.set(response.items));
  }
}
