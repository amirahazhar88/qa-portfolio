// Allure 3 configuration. Run through scripts/report.sh (or see README "Test report").
export default {
  name: 'newsclip test report',
  output: './allure-report',
  // Run history (trends) is stored here; CI keeps it between runs.
  historyPath: './allure-history.jsonl',
  plugins: {
    awesome: {
      options: {
        reportName: 'newsclip test report',
        reportLanguage: 'en',
      },
    },
  },
};
