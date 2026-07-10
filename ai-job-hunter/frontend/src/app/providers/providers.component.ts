import { Component, OnInit, inject, signal } from "@angular/core";
import { ApiService } from "@core/services/api.service";

interface ProviderStatus {
  id: string;
  name: string;
  slug: string;
  base_url: string;
  health_status: string;
  last_sync_at: string | null;
  last_error: string | null;
  jobs_found: number;
}

@Component({
  selector: "ajh-providers",
  standalone: true,
  template: `
    <h1 class="text-3xl font-bold">Live sources</h1>
    <p class="text-[var(--text-muted)] mt-2">
      Only official APIs and feeds are used. Provider failures are isolated and
      visible here.
    </p>
    <div class="grid md:grid-cols-2 gap-4 mt-8">
      @for (provider of providers(); track provider.id) {
        <article
          class="rounded-xl border border-[var(--border-color)] bg-surface-800 p-5"
        >
          <div class="flex justify-between gap-3">
            <div>
              <h2 class="font-semibold text-lg">{{ provider.name }}</h2>
              <a
                [href]="provider.base_url"
                target="_blank"
                rel="noopener"
                class="text-xs text-brand-300"
                >Official source</a
              >
            </div>
            <span
              class="text-xs rounded-full px-2.5 py-1 h-fit"
              [class.text-brand-300]="provider.health_status === 'healthy'"
              [class.text-amber-300]="provider.health_status !== 'healthy'"
              >{{ provider.health_status }}</span
            >
          </div>
          <p class="text-2xl font-bold mt-5">{{ provider.jobs_found }}</p>
          <p class="text-xs text-[var(--text-muted)]">
            fresh jobs accepted in the last sync
          </p>
          @if (provider.last_error) {
            <p class="text-xs text-red-400 mt-3">{{ provider.last_error }}</p>
          }
        </article>
      } @empty {
        <p class="text-[var(--text-muted)]">
          Run a job sync to initialize providers.
        </p>
      }
    </div>
  `,
})
export class ProvidersComponent implements OnInit {
  private readonly api = inject(ApiService);
  readonly providers = signal<ProviderStatus[]>([]);
  ngOnInit(): void {
    this.api
      .get<ProviderStatus[]>("/providers")
      .subscribe((items) => this.providers.set(items));
  }
}
