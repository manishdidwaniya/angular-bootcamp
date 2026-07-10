import { Component, OnInit, inject } from "@angular/core";

import {
  NotificationItem,
  NotificationService,
} from "@core/services/notification.service";

@Component({
  selector: "ajh-notifications",
  standalone: true,
  template: `
    <h1 class="text-3xl font-bold">Notifications</h1>
    <p class="text-[var(--text-muted)] mt-2">
      Fresh matches meeting your score threshold appear here.
    </p>
    <div class="grid gap-3 mt-7">
      @for (item of notifications.items(); track item.id) {
        <button
          (click)="read(item)"
          class="text-left rounded-xl border p-5 transition-colors"
          [class.border-brand-300]="!item.is_read"
          [class.border-[var(--border-color)]]="item.is_read"
          [class.bg-surface-800]="item.is_read"
          [class.bg-surface-700]="!item.is_read"
        >
          <div class="flex justify-between gap-4">
            <strong>{{ item.title }}</strong
            ><span class="text-xs uppercase text-brand-300">{{
              item.channel
            }}</span>
          </div>
          <p class="text-[var(--text-muted)] mt-2 whitespace-pre-line">
            {{ item.message }}
          </p>
          <p class="text-xs text-[var(--text-muted)] mt-3">
            {{ item.created_at.slice(0, 16).replace("T", " ") }}
          </p>
        </button>
      } @empty {
        <p class="text-[var(--text-muted)]">
          No alerts yet. Sync jobs after completing your profile.
        </p>
      }
    </div>
  `,
})
export class NotificationsComponent implements OnInit {
  readonly notifications = inject(NotificationService);
  ngOnInit(): void {
    this.notifications.refresh();
  }
  read(item: NotificationItem): void {
    this.notifications.markRead(item);
  }
}
