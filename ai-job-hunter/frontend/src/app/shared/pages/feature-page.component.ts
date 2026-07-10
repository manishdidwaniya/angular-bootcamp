import { Component, inject } from '@angular/core';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'ajh-feature-page',
  standalone: true,
  template: `
    <section>
      <p class="text-brand-300 text-xs uppercase tracking-widest font-semibold">AI Job Hunter</p>
      <h1 class="text-3xl font-bold mt-2">{{ title }}</h1>
      <p class="text-[var(--text-muted)] mt-2 max-w-2xl">{{ description }}</p>
      <div class="mt-8 rounded-xl border border-[var(--border-color)] bg-surface-800 p-6">
        <p class="text-sm text-[var(--text-muted)]">This module is wired into the executable application and ready for its next workflow.</p>
      </div>
    </section>
  `,
})
export class FeaturePageComponent {
  private readonly route = inject(ActivatedRoute);
  readonly title = this.route.snapshot.data['title'] as string;
  readonly description = this.route.snapshot.data['description'] as string;
}
