import { Component, OnInit, inject, signal } from "@angular/core";

import { ApiService } from "@core/services/api.service";

interface TrackedApplication {
  id: string;
  status: string;
  created_at: string;
  job: { title: string; company: string; url: string };
}

@Component({
  selector: "ajh-applications",
  standalone: true,
  template: `
    <h1 class="text-3xl font-bold">Applications</h1>
    <p class="text-[var(--text-muted)] mt-2">
      Keep every application and next step in one place.
    </p>
    @if (error()) {
      <p class="text-red-400 mt-4">{{ error() }}</p>
    }
    <div class="grid gap-4 mt-7">
      @for (item of applications(); track item.id) {
        <article
          class="rounded-xl border border-[var(--border-color)] bg-surface-800 p-5 flex flex-wrap gap-4 items-center"
        >
          <div class="flex-1 min-w-64">
            <a
              [href]="item.job.url"
              target="_blank"
              rel="noopener"
              class="text-lg font-semibold hover:text-brand-300"
              >{{ item.job.title }}</a
            >
            <p class="text-[var(--text-muted)]">
              {{ item.job.company }} · tracked
              {{ item.created_at.slice(0, 10) }}
            </p>
          </div>
          <select
            [value]="item.status"
            (change)="changeStatus(item, $event)"
            class="field max-w-48"
          >
            <option value="applied">Applied</option>
            <option value="interviewing">Interviewing</option>
            <option value="offered">Offered</option>
            <option value="rejected">Rejected</option>
            <option value="withdrawn">Withdrawn</option>
          </select>
        </article>
      } @empty {
        <p class="text-[var(--text-muted)]">
          No tracked applications yet. Use Track on a job first.
        </p>
      }
    </div>
  `,
  styles: [
    `
      .field {
        border: 1px solid var(--border-color);
        border-radius: 0.5rem;
        background: var(--surface-900);
        padding: 0.65rem 0.8rem;
      }
    `,
  ],
})
export class ApplicationsComponent implements OnInit {
  private api = inject(ApiService);
  applications = signal<TrackedApplication[]>([]);
  error = signal("");
  ngOnInit(): void {
    this.load();
  }
  load(): void {
    this.api.get<TrackedApplication[]>("/applications").subscribe({
      next: (data) => this.applications.set(data),
      error: () => this.error.set("Unable to load applications."),
    });
  }
  changeStatus(item: TrackedApplication, event: Event): void {
    const status = (event.target as HTMLSelectElement).value;
    this.api
      .patch<TrackedApplication>(`/applications/${item.id}`, { status })
      .subscribe({
        next: (updated) =>
          this.applications.update((items) =>
            items.map((current) =>
              current.id === updated.id ? updated : current,
            ),
          ),
        error: () => this.error.set("Unable to update application status."),
      });
  }
}
