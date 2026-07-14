import { defineConfig, devices } from '@playwright/test';

const executablePath = process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH;
const launchOptions = executablePath ? { executablePath } : undefined;
const python = process.env.PYTHON_EXECUTABLE || 'python3';
const useExternalServer = process.env.PLAYWRIGHT_EXTERNAL_SERVER === '1';

export default defineConfig({
  testDir: './tests',
  timeout: 60_000,
  retries: 1,
  reporter: [['list'], ['html', { open: 'never' }]],
  use: {
    baseURL: 'http://127.0.0.1:4173',
    trace: 'retain-on-failure'
  },
  webServer: useExternalServer ? undefined : {
    command: `"${python}" -m http.server 4173 -d _site`,
    url: 'http://127.0.0.1:4173',
    reuseExistingServer: !process.env.CI,
    timeout: 30_000
  },
  projects: [
    { name: 'desktop-chromium', use: { ...devices['Desktop Chrome'], launchOptions } },
    { name: 'tablet-chromium', use: { ...devices['iPad Pro 11'], browserName: 'chromium', launchOptions } },
    { name: 'mobile-chromium', use: { ...devices['Pixel 5'], launchOptions } }
  ]
});
