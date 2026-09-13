import { useEffect } from 'react';

interface KeyboardShortcutHandlers {
  onOpenCommandPalette: () => void;
  onOpenChat: () => void;
  onRefresh: () => void;
  onRunDemo: () => void;
}

export function useKeyboardShortcuts({
  onOpenCommandPalette,
  onOpenChat,
  onRefresh,
  onRunDemo,
}: KeyboardShortcutHandlers) {
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      // Ignore if user is currently typing in an input field
      if (['INPUT', 'TEXTAREA', 'SELECT'].includes((e.target as HTMLElement)?.tagName)) {
        return;
      }

      if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'k') {
        e.preventDefault();
        onOpenCommandPalette();
      } else if (e.key.toLowerCase() === 'c') {
        onOpenChat();
      } else if (e.key.toLowerCase() === 'r') {
        onRefresh();
      } else if (e.key.toLowerCase() === 'd') {
        onRunDemo();
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [onOpenCommandPalette, onOpenChat, onRefresh, onRunDemo]);
}
