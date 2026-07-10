/** 认证服务 — 处理登录、注册、token 管理。 */

import { Injectable, computed, inject, signal } from '@angular/core';
import { Observable } from 'rxjs';
import { ApiService } from './api.service';
import {
  User,
  UserWithTokens,
  LoginRequest,
  RegisterRequest,
} from '../models/user.model';

const TOKEN_KEY = 'ajh_access_token';
const REFRESH_KEY = 'ajh_refresh_token';
const USER_KEY = 'ajh_user';

@Injectable({ providedIn: 'root' })
export class AuthService {
  private api = inject(ApiService);

  readonly currentUser = signal<User | null>(this.loadUser());
  readonly isLoggedIn = computed(() => !!this.currentUser());
  readonly isAdmin = computed(() => this.currentUser()?.role === 'admin');

  register(data: RegisterRequest): Observable<UserWithTokens> {
    return this.api.post<UserWithTokens>('/auth/register', data);
  }

  login(data: LoginRequest): Observable<UserWithTokens> {
    return this.api.post<UserWithTokens>('/auth/login', data);
  }

  logout(): void {
    localStorage.removeItem(TOKEN_KEY);
    localStorage.removeItem(REFRESH_KEY);
    localStorage.removeItem(USER_KEY);
    this.currentUser.set(null);
  }

  handleAuthResponse(response: UserWithTokens): void {
    this.setTokens(response.access_token, response.refresh_token);
    this.currentUser.set(response.user);
    localStorage.setItem(USER_KEY, JSON.stringify(response.user));
  }

  getAccessToken(): string | null {
    return localStorage.getItem(TOKEN_KEY);
  }

  private setTokens(access: string, refresh: string): void {
    localStorage.setItem(TOKEN_KEY, access);
    localStorage.setItem(REFRESH_KEY, refresh);
  }

  private loadUser(): User | null {
    try {
      const stored = localStorage.getItem(USER_KEY);
      return stored ? JSON.parse(stored) : null;
    } catch {
      return null;
    }
  }
}
