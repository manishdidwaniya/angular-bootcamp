import { Component, OnInit, inject, signal } from "@angular/core";
import { FormBuilder, ReactiveFormsModule, Validators } from "@angular/forms";
import { ApiService } from "@core/services/api.service";

interface Resume {
  id: string;
  title: string;
  parsed_content: string | null;
  is_primary: boolean;
  is_active: boolean;
}

@Component({
  selector: "ajh-resumes",
  standalone: true,
  imports: [ReactiveFormsModule],
  template: `
    <div class="max-w-4xl">
      <h1 class="text-3xl font-bold">Resumes</h1>
      <p class="text-[var(--text-muted)] mt-2">
        Paste resume text so matching can suggest the most relevant version for
        each job.
      </p>
      <form
        [formGroup]="form"
        (ngSubmit)="add()"
        class="mt-7 rounded-xl border border-[var(--border-color)] bg-surface-800 p-5 space-y-4"
      >
        <label class="text-sm"
          >Resume name<input
            formControlName="title"
            class="field"
            placeholder="Product resume" /></label
        ><label class="text-sm"
          >Resume text<textarea
            formControlName="parsed_content"
            rows="10"
            class="field"
            placeholder="Paste the full text from your resume"
          ></textarea></label
        ><label class="flex items-center gap-2 text-sm"
          ><input type="checkbox" formControlName="is_primary" /> Use as primary
          resume</label
        ><button
          type="submit"
          [disabled]="form.invalid || saving()"
          class="rounded-lg bg-brand-300 text-surface-900 px-5 py-2.5 font-semibold disabled:opacity-50"
        >
          Add resume
        </button>
      </form>
      <div class="grid gap-3 mt-6">
        @for (resume of resumes(); track resume.id) {
          <article
            class="rounded-xl border border-[var(--border-color)] bg-surface-800 p-4 flex justify-between gap-4"
          >
            <div>
              <h2 class="font-semibold">{{ resume.title }}</h2>
              <p class="text-xs text-[var(--text-muted)] mt-1">
                {{ resume.parsed_content?.length || 0 }} characters
                @if (resume.is_primary) {
                  · Primary
                }
              </p>
            </div>
            <button (click)="remove(resume.id)" class="text-sm text-red-400">
              Delete
            </button>
          </article>
        }
      </div>
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
        background: var(--surface-bg);
        color: white;
      }
    `,
  ],
})
export class ResumesComponent implements OnInit {
  private readonly api = inject(ApiService);
  private readonly fb = inject(FormBuilder);
  readonly resumes = signal<Resume[]>([]);
  readonly saving = signal(false);
  readonly form = this.fb.nonNullable.group({
    title: ["", Validators.required],
    parsed_content: ["", [Validators.required, Validators.minLength(50)]],
    is_primary: false,
  });
  ngOnInit(): void {
    this.load();
  }
  load(): void {
    this.api.get<Resume[]>("/resumes").subscribe({
      next: (items) => this.resumes.set(items),
      error: () => this.resumes.set([]),
    });
  }
  add(): void {
    if (this.form.invalid) return;
    this.saving.set(true);
    this.api.post<Resume>("/resumes", this.form.getRawValue()).subscribe({
      next: () => {
        this.saving.set(false);
        this.form.reset({ title: "", parsed_content: "", is_primary: false });
        this.load();
      },
      error: () => this.saving.set(false),
    });
  }
  remove(id: string): void {
    this.api.delete(`/resumes/${id}`).subscribe(() => this.load());
  }
}
