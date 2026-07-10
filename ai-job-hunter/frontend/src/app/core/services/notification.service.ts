import { Injectable, inject, signal } from "@angular/core";

import { ApiService } from "./api.service";

export interface NotificationItem {
  id: string;
  title: string;
  message: string;
  channel: string;
  is_read: boolean;
  created_at: string;
}

@Injectable({ providedIn: "root" })
export class NotificationService {
  private readonly api = inject(ApiService);
  readonly items = signal<NotificationItem[]>([]);
  readonly unreadCount = signal(0);

  refresh(): void {
    this.api.get<NotificationItem[]>("/notifications").subscribe({
      next: (items) => this.setItems(items),
      error: () => this.setItems([]),
    });
  }

  markRead(item: NotificationItem): void {
    if (item.is_read) return;
    this.api
      .patch<NotificationItem>(`/notifications/${item.id}/read`)
      .subscribe((updated) =>
        this.setItems(
          this.items().map((current) =>
            current.id === updated.id ? updated : current,
          ),
        ),
      );
  }

  private setItems(items: NotificationItem[]): void {
    this.items.set(items);
    this.unreadCount.set(items.filter((item) => !item.is_read).length);
  }
}
