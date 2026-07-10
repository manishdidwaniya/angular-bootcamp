/** 主布局组件 — 侧边栏 + 顶栏 + 内容区。 */

import { Component, OnInit, inject, signal } from "@angular/core";
import { RouterOutlet, RouterLink, RouterLinkActive } from "@angular/router";
import { AuthService } from "@core/services/auth.service";
import { NotificationService } from "@core/services/notification.service";

interface NavItem {
  label: string;
  route: string;
  icon: string;
}

@Component({
  selector: "ajh-layout",
  imports: [RouterOutlet, RouterLink, RouterLinkActive],
  template: `
    <div class="flex h-screen overflow-hidden">
      <!-- 侧边栏 -->
      <aside
        class="w-64 bg-surface-800 border-r border-[var(--border-color)] flex flex-col flex-shrink-0 transition-transform"
        [class.-translate-x-full]="!sidebarOpen()"
        [class.absolute]="!sidebarOpen()"
        [class.z-50]="!sidebarOpen()"
      >
        <!-- Logo -->
        <div class="p-5 border-b border-[var(--border-color)]">
          <div class="flex items-center gap-3">
            <div
              class="w-9 h-9 rounded-lg bg-brand-300 flex items-center justify-center"
            >
              <i class="fa-solid fa-crosshairs text-surface-900 text-sm"></i>
            </div>
            <span class="font-bold text-lg tracking-tight">AI Job Hunter</span>
          </div>
        </div>

        <!-- 导航 -->
        <nav class="flex-1 py-4 overflow-y-auto">
          @for (item of navItems; track item.route) {
            <a
              [routerLink]="item.route"
              routerLinkActive="bg-[var(--brand-primary-dim)] text-brand-300"
              class="flex items-center gap-3 px-5 py-2.5 text-sm text-[var(--text-muted)] hover:text-white hover:bg-surface-700 transition-colors"
            >
              <i class="fa-solid w-5 text-center" [class]="item.icon"></i>
              <span>{{ item.label }}</span>
            </a>
          }
        </nav>

        <!-- 用户信息 -->
        <div class="p-4 border-t border-[var(--border-color)]">
          <button
            (click)="authService.logout()"
            class="flex items-center gap-3 w-full px-3 py-2 text-sm text-[var(--text-muted)] hover:text-red-400 rounded-lg hover:bg-surface-700 transition-colors"
          >
            <i class="fa-solid fa-right-from-bracket w-5 text-center"></i>
            <span>Sign Out</span>
          </button>
        </div>
      </aside>

      <!-- 主内容 -->
      <div class="flex-1 flex flex-col overflow-hidden">
        <!-- 顶栏 -->
        <header
          class="h-14 bg-surface-800 border-b border-[var(--border-color)] flex items-center px-6 gap-4 flex-shrink-0"
        >
          <button
            (click)="sidebarOpen.set(!sidebarOpen())"
            class="lg:hidden text-[var(--text-muted)]"
          >
            <i class="fa-solid fa-bars"></i>
          </button>
          <div class="flex-1"></div>
          <!-- 通知图标 -->
          <a
            routerLink="/notifications"
            (click)="notifications.refresh()"
            aria-label="Open notifications"
            class="relative text-[var(--text-muted)] hover:text-white transition-colors"
          >
            <i class="fa-solid fa-bell text-lg"></i>
            @if (notifications.unreadCount() > 0) {
              <span
                class="absolute -top-2 -right-2 min-w-4 h-4 px-1 bg-brand-300 rounded-full text-[10px] text-surface-900 flex items-center justify-center font-bold"
                >{{
                  notifications.unreadCount() > 99
                    ? "99+"
                    : notifications.unreadCount()
                }}</span
              >
            }
          </a>
        </header>

        <!-- 内容 -->
        <main class="flex-1 overflow-y-auto p-6">
          <router-outlet />
        </main>
      </div>
    </div>
  `,
})
export class LayoutComponent implements OnInit {
  authService = inject(AuthService);
  readonly notifications = inject(NotificationService);
  sidebarOpen = signal(window.innerWidth >= 1024);

  ngOnInit(): void {
    this.notifications.refresh();
  }

  readonly navItems: NavItem[] = [
    { label: "Dashboard", route: "/dashboard", icon: "fa-chart-line" },
    { label: "Jobs", route: "/jobs", icon: "fa-briefcase" },
    { label: "Profiles", route: "/profiles", icon: "fa-user-pen" },
    { label: "Resumes", route: "/resumes", icon: "fa-file-lines" },
    { label: "Job Sources", route: "/providers", icon: "fa-satellite-dish" },
    { label: "Applications", route: "/applications", icon: "fa-paper-plane" },
    { label: "Analytics", route: "/analytics", icon: "fa-chart-pie" },
    { label: "Notifications", route: "/notifications", icon: "fa-bell" },
    { label: "Settings", route: "/settings", icon: "fa-gear" },
    { label: "Admin", route: "/admin", icon: "fa-shield-halved" },
  ];
}
