import { defineConfig } from 'vitest/config';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: './tests/setup.ts',
    css: true,
    reporters: ['verbose', 'junit'],
    outputFile: {
      junit: './reports/junit.xml'
    },
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html'],
      exclude: [
        'node_modules/',
        'tests/',
        'src/types/',
        'src/stories/',
        'src/assets/',
        '**/index.ts',
        '**/types.ts',
        '**/__generated__/**',
        '**/*.stories.tsx',
        '**/*.d.ts',
        'src/main.tsx',
        'src/App.tsx'
      ]
    }
  },
  resolve: {
    alias: {
      '@': '/src',
    },
  },
});