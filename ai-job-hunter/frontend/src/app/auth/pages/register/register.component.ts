import { Component, inject, signal } from '@angular/core';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';

import { AuthService } from '@core/services/auth.service';

@Component({
    selector: 'ajh-register',
    imports: [ReactiveFormsModule, RouterLink],
    template: `
    <div class="min-h-screen flex items-center justify-center px-4">
      <div class="w-full max-w-md rounded-2xl border border-[var(--border-color)] bg-surface-800 p-8">
        <h1 class="text-2xl font-bold">Create your account</h1>
        <p class="text-sm text-[var(--text-muted)] mt-1 mb-6">Start organizing your job search.</p>
        <form [formGroup]="form" (ngSubmit)="submit()" class="space-y-4">
          <label class="block text-sm">Full name
            <input formControlName="full_name" class="mt-1 w-full rounded-lg bg-surface-900 border border-[var(--border-color)] px-4 py-2.5" />
          </label>
          <label class="block text-sm">Email
            <input type="email" formControlName="email" class="mt-1 w-full rounded-lg bg-surface-900 border border-[var(--border-color)] px-4 py-2.5" />
          </label>
          <label class="block text-sm">Password
            <input type="password" formControlName="password" class="mt-1 w-full rounded-lg bg-surface-900 border border-[var(--border-color)] px-4 py-2.5" />
          </label>
          @if (error()) { <p class="text-sm text-red-400">{{ error() }}</p> }
          <button type="submit" [disabled]="form.invalid || loading()" class="w-full rounded-lg bg-brand-300 text-surface-900 font-semibold py-2.5 disabled:opacity-50">
            {{ loading() ? 'Creating account...' : 'Create account' }}
          </button>
        </form>
        <p class="text-sm text-center text-[var(--text-muted)] mt-5">Already registered? <a routerLink="/auth/login" class="text-brand-300">Sign in</a></p>
      </div>
    </div>
  `
})
export class RegisterComponent {
  private readonly fb = inject(FormBuilder);
  private readonly auth = inject(AuthService);
  private readonly router = inject(Router);

  readonly loading = signal(false);
  readonly error = signal<string | null>(null);
  readonly form = this.fb.nonNullable.group({
    full_name: ['', [Validators.required, Validators.maxLength(255)]],
    email: ['', [Validators.required, Validators.email]],
    password: ['', [Validators.required, Validators.minLength(8), Validators.maxLength(128)]],
  });

  submit(): void {
    if (this.form.invalid) return;
    this.loading.set(true);
    this.error.set(null);
    this.auth.register(this.form.getRawValue()).subscribe({
      next: response => {
        this.auth.handleAuthResponse(response);
        void this.router.navigate(['/dashboard']);
      },
      error: err => {
        this.error.set(err.error?.error?.message ?? 'Registration failed.');
        this.loading.set(false);
      },
    });
  }
}
