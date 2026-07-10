import { Component, OnInit, inject, signal } from "@angular/core";
import { FormBuilder, ReactiveFormsModule } from "@angular/forms";
import { ApiService } from "@core/services/api.service";

interface Preferences {
  freshness_days: number;
  min_match_score: number;
  search_terms: string[];
  locations: string[];
  work_modes: string[];
  email_enabled: boolean;
  telegram_enabled: boolean;
  slack_enabled: boolean;
  discord_enabled: boolean;
  telegram_chat_id: string | null;
  slack_webhook_url: string | null;
  discord_webhook_url: string | null;
}

@Component({
  selector: "ajh-settings",
  standalone: true,
  imports: [ReactiveFormsModule],
  template: `
    <div class="max-w-3xl">
      <h1 class="text-3xl font-bold">Search & notification settings</h1>
      <p class="text-[var(--text-muted)] mt-2">
        Control how fresh a job must be and when a match deserves an alert.
      </p>
      <form
        [formGroup]="form"
        (ngSubmit)="save()"
        class="grid md:grid-cols-2 gap-5 mt-8"
      >
        <label class="text-sm"
          >Maximum job age<select
            formControlName="freshness_days"
            class="field"
          >
            <option [value]="1">24 hours</option>
            <option [value]="3">3 days</option>
            <option [value]="7">7 days</option>
            <option [value]="14">14 days</option>
          </select></label
        ><label class="text-sm"
          >Minimum alert match score<input
            type="number"
            min="0"
            max="100"
            formControlName="min_match_score"
            class="field" /></label
        ><label class="text-sm md:col-span-2"
          >Search terms<input
            formControlName="search_terms"
            class="field"
            placeholder="Product Manager, Business Analyst" /></label
        ><label class="text-sm md:col-span-2"
          >Locations<input
            formControlName="locations"
            class="field"
            placeholder="Bengaluru, Remote"
        /></label>
        <div
          class="md:col-span-2 grid sm:grid-cols-2 gap-3 rounded-xl border border-[var(--border-color)] p-4"
        >
          <label class="flex gap-2"
            ><input type="checkbox" formControlName="email_enabled" /> Email
            alerts</label
          ><label class="flex gap-2"
            ><input type="checkbox" formControlName="telegram_enabled" />
            Telegram alerts</label
          ><label class="flex gap-2"
            ><input type="checkbox" formControlName="slack_enabled" /> Slack
            alerts</label
          ><label class="flex gap-2"
            ><input type="checkbox" formControlName="discord_enabled" /> Discord
            alerts</label
          >
        </div>
        <label class="text-sm"
          >Telegram chat ID<input
            formControlName="telegram_chat_id"
            class="field" /></label
        ><label class="text-sm"
          >Slack webhook<input
            formControlName="slack_webhook_url"
            class="field" /></label
        ><label class="text-sm md:col-span-2"
          >Discord webhook<input
            formControlName="discord_webhook_url"
            class="field"
        /></label>
        <div class="md:col-span-2">
          <button
            type="submit"
            class="rounded-lg bg-brand-300 text-surface-900 px-5 py-2.5 font-semibold"
          >
            Save settings
          </button>
          @if (saved()) {
            <span class="text-sm text-brand-300 ml-3">Saved.</span>
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
export class SettingsComponent implements OnInit {
  private readonly api = inject(ApiService);
  private readonly fb = inject(FormBuilder);
  readonly saved = signal(false);
  readonly form = this.fb.nonNullable.group({
    freshness_days: 7,
    min_match_score: 60,
    search_terms: "",
    locations: "",
    email_enabled: false,
    telegram_enabled: false,
    slack_enabled: false,
    discord_enabled: false,
    telegram_chat_id: "",
    slack_webhook_url: "",
    discord_webhook_url: "",
  });
  ngOnInit(): void {
    this.api.get<Preferences>("/settings/me").subscribe((value) =>
      this.form.patchValue({
        ...value,
        search_terms: value.search_terms.join(", "),
        locations: value.locations.join(", "),
        telegram_chat_id: value.telegram_chat_id ?? "",
        slack_webhook_url: value.slack_webhook_url ?? "",
        discord_webhook_url: value.discord_webhook_url ?? "",
      }),
    );
  }
  save(): void {
    const value = this.form.getRawValue();
    const csv = (text: string) =>
      text
        .split(",")
        .map((item) => item.trim())
        .filter(Boolean);
    this.api
      .put<Preferences>("/settings/me", {
        ...value,
        search_terms: csv(value.search_terms),
        locations: csv(value.locations),
        work_modes: [],
      })
      .subscribe(() => {
        this.saved.set(true);
        setTimeout(() => this.saved.set(false), 2000);
      });
  }
}
