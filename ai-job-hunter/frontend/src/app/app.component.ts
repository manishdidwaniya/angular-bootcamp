import { Component, signal } from '@angular/core';
import { RouterOutlet } from '@angular/router';

@Component({
    selector: 'ajh-root',
    imports: [RouterOutlet],
    template: `
    <div class="min-h-screen bg-surface-900">
      <router-outlet />
    </div>
  `,
    styles: [':host { display: block; }']
})
export class AppComponent {
  readonly isDark = signal(true);
}