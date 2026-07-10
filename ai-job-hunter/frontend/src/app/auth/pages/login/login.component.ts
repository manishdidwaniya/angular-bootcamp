/** 登录页面。 */

import { Component, inject, signal } from '@angular/core';
import { ReactiveFormsModule, FormBuilder, Validators, FormGroup } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';
import { AuthService } from '@core/services/auth.service';

@Component({
    selector: 'ajh-login',
    imports: [ReactiveFormsModule, RouterLink],
    template: `
    <div class="min-h-screen flex items-center justify-center bg-surface-900 px-4">
      <div class="w-full max-w-md">
        <!-- Logo -->
        <div class="text-center mb-8">
          <div class="w-16 h-16 rounded-2xl bg-brand-300 flex items-center justify-center mx-auto mb-4">
            <i class="fa-solid fa-crosshairs text-surface-900 text-2xl"></i>
          </div>
          <h1 class="text-2xl font-bold">Welcome back</h1>
          <p class="text-[var(--text-muted)] mt-1">Sign in to AI Job Hunter</p>
        </div>

        <!-- 表单 -->
        <form [formGroup]="form" (ngSubmit)="onSubmit()" class="space-y-4">
          <div>
            <label for="login-email" class="block text-sm font-medium mb-1.5">Email</label>
            <input
              id="login-email"
              type="email"
              formControlName="email"
              placeholder="you@example.com"
              class="w-full px-4 py-2.5 bg-surface-800 border border-[var(--border-color)] rounded-lg text-white placeholder-[var(--text-muted)] focus:outline-none focus:border-brand-300 transition-colors"
            >
          </div>

          <div>
            <label for="login-password" class="block text-sm font-medium mb-1.5">Password</label>
            <input
              id="login-password"
              type="password"
              formControlName="password"
              placeholder="Enter your password"
              class="w-full px-4 py-2.5 bg-surface-800 border border-[var(--border-color)] rounded-lg text-white placeholder-[var(--text-muted)] focus:outline-none focus:border-brand-300 transition-colors"
            >
          </div>

          @if (error()) {
            <div class="text-red-400 text-sm bg-red-400/10 border border-red-400/20 rounded-lg px-4 py-2">
              {{ error() }}
            </div>
          }

          <button
            type="submit"
            [disabled]="form.invalid || loading()"
            class="w-full py-2.5 bg-brand-300 text-surface-900 font-semibold rounded-lg hover:bg-brand-400 transition-colors disabled:opacity-50"
          >
            @if (loading()) { Signing in... } @else { Sign In }
          </button>
        </form>

        <p class="text-center text-sm text-[var(--text-muted)] mt-6">
          Don't have an account?
          <a routerLink="/auth/register" class="text-brand-300 hover:underline">Create one</a>
        </p>
      </div>
    </div>
  `
})
export class LoginComponent {
  private fb = inject(FormBuilder);
  private authService = inject(AuthService);
  private router = inject(Router);

  form: FormGroup = this.fb.group({
    email: ['', [Validators.required, Validators.email]],
    password: ['', [Validators.required, Validators.minLength(8)]],
  });

  loading = signal(false);
  error = signal<string | null>(null);

  onSubmit(): void {
    if (this.form.invalid) return;
    this.loading.set(true);
    this.error.set(null);

    this.authService.login(this.form.value).subscribe({
      next: (response) => {
        this.authService.handleAuthResponse(response);
        this.router.navigate(['/dashboard']);
      },
      error: (err) => {
        this.error.set(err.error?.error?.message || 'Login failed.');
        this.loading.set(false);
      },
      complete: () => this.loading.set(false),
    });
  }
}
