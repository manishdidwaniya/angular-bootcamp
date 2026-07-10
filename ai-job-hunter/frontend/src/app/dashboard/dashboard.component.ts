import { Component, OnInit, inject, signal } from '@angular/core';

import { ApiService } from '@core/services/api.service';

interface Summary {
  applications: number;
  active_jobs: number;
  unread_notifications: number;
}

@Component({
  selector: 'ajh-dashboard',
  standalone: true,
  template: `
    <h1 class="text-3xl font-bold">Dashboard</h1>
    <p class="text-[var(--text-muted)] mt-2">Your job-search activity at a glance.</p>
    <div class="grid sm:grid-cols-3 gap-4 mt-8">
      @for (card of cards(); track card.label) {
        <article class="rounded-xl border border-[var(--border-color)] bg-surface-800 p-6">
          <p class="text-sm text-[var(--text-muted)]">{{ card.label }}</p>
          <p class="text-3xl font-bold mt-2 text-brand-300">{{ card.value }}</p>
        </article>
      }
    </div>
    @if (error()) { <p class="text-red-400 text-sm mt-4">{{ error() }}</p> }
  `,
})
export class DashboardComponent implements OnInit {
  private readonly api = inject(ApiService);
  readonly summary = signal<Summary>({ applications: 0, active_jobs: 0, unread_notifications: 0 });
  readonly error = signal<string | null>(null);
  readonly cards = () => [
    { label: 'Applications', value: this.summary().applications },
    { label: 'Active jobs', value: this.summary().active_jobs },
    { label: 'Unread notifications', value: this.summary().unread_notifications },
  ];

  ngOnInit(): void {
    this.api.get<Summary>('/analytics/summary').subscribe({
      next: summary => this.summary.set(summary),
      error: () => this.error.set('Dashboard data is currently unavailable.'),
    });
  }
}
