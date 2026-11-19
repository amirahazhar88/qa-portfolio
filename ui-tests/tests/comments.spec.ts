import { test, expect } from '../fixtures';
import { buildComment } from '../test-data/factory';

test.describe('Comments', () => {
  test('a signed-in user can post a comment', { tag: '@smoke' }, async ({
    authedPage,
    articlePage,
    authorArticle,
  }) => {
    const body = buildComment();
    await articlePage.goto(authorArticle.slug);

    await articlePage.commentInput.fill(body);
    await articlePage.postCommentButton.click();

    await expect(articlePage.comments).toHaveText([body]);
    await expect(articlePage.commentInput).toHaveValue('');
  });

  test('an empty comment is rejected', async ({ authedPage, articlePage, authorArticle }) => {
    await articlePage.goto(authorArticle.slug);

    await articlePage.postCommentButton.click();

    await expect(articlePage.commentErrors.first()).toBeVisible();
    await expect(articlePage.comments).toHaveCount(0);
  });

  test('a user can delete their own comment', async ({
    authedPage,
    articlePage,
    authorArticle,
    api,
    user,
  }) => {
    const body = buildComment();
    await api.addComment(user.token, authorArticle.slug, body);
    await articlePage.goto(authorArticle.slug);
    await expect(articlePage.comments).toHaveText([body]);

    await articlePage.commentDeleteIcons.click();

    await expect(articlePage.comments).toHaveCount(0);
  });

  test('a deleted comment stays gone after a reload', async ({
    authedPage,
    articlePage,
    authorArticle,
    api,
    user,
  }) => {
    // Known bug: the API answers 200 but keeps the comment, so it comes back (docs/bugs/BUG-007.md).
    // The UI removes it from the screen without checking the server, so only a reload shows the truth.
    // Remove test.fail() once BUG-007 is fixed.
    test.fail(true, 'BUG-007: DELETE comment returns 200 but the comment is not removed');

    await api.addComment(user.token, authorArticle.slug, buildComment());
    await articlePage.goto(authorArticle.slug);
    await articlePage.commentDeleteIcons.click();
    await expect(articlePage.comments).toHaveCount(0);

    // The list is empty while it loads, so wait for the comments request before asserting.
    await Promise.all([
      authedPage.waitForResponse((r) => r.url().endsWith('/comments') && r.request().method() === 'GET'),
      authedPage.reload(),
    ]);

    await expect(articlePage.comments).toHaveCount(0);
  });

  test("other users' comments are listed without a delete control", async ({
    authedPage,
    articlePage,
    authorArticle,
    author,
    api,
  }) => {
    const body = buildComment();
    await api.addComment(author.token, authorArticle.slug, body);

    await articlePage.goto(authorArticle.slug);

    await expect(articlePage.comments).toHaveText([body]);
    await expect(articlePage.commentDeleteIcons).toHaveCount(0);
  });

  test('a signed-out visitor sees a sign-in prompt instead of the comment box', async ({
    page,
    articlePage,
    authorArticle,
  }) => {
    await articlePage.goto(authorArticle.slug);

    await expect(articlePage.signInPrompt).toBeVisible();
    await expect(articlePage.commentInput).toHaveCount(0);
  });
});
