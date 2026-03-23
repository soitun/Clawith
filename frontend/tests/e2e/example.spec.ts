import { test, expect } from '@playwright/test';

test('has title', async ({ page }) => {
  // Since the app likely requires authentication, we'll just check that the page loads
  await page.goto('/');

  // Expect a title "to contain" a substring.
  await expect(page).toHaveTitle(/Clawith/);
});

test('get started link', async ({ page }) => {
  await page.goto('/');

  // Click the get started link
  await page.getByRole('link', { name: 'Get started' }).click();

  // Expects the URL to contain intro.
  await expect(page).toHaveURL(/.*intro/);
});