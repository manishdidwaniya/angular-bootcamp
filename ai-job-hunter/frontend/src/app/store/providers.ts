/** 状态管理 Providers — 使用 Angular Signals + inject()。 */

import { Provider } from "@angular/core";

/** 简易信号状态容器 */
export interface SignalState<T> {
  value: T;
  set(newValue: T): void;
  update(updater: (current: T) => T): void;
}

export function signalState<T>(initial: T): SignalState<T> {
  let currentValue = initial;
  const listeners = new Set<(val: T) => void>();

  return {
    get value() {
      return currentValue;
    },
    set(newValue: T) {
      currentValue = newValue;
      listeners.forEach((fn) => fn(currentValue));
    },
    update(updater: (current: T) => T) {
      currentValue = updater(currentValue);
      listeners.forEach((fn) => fn(currentValue));
    },
  };
}

export function provideStore(): Provider[] {
  return [];
}
