# newsclip test cases

> **Generated** by `python3 scripts/gen_test_cases.py` from the real tests. Do not edit by hand; change the tests and regenerate.

Generated on 2026-11-19: **135 automated test cases** (46 UI, 89 API), of which **14** cover a known defect and are expected to fail until it is fixed. SQL checks are listed in [`sql/README.md`](../sql/README.md).

How to read it: *Covers* uses the feature IDs (F1 to F17) of the [coverage matrix](test-plan.md). *Known defect* links to the bug report; those tests are written to fail until the bug is fixed (`test.fail()` in Playwright, `xfail(strict=True)` in pytest).

## UI tests (Playwright, `ui-tests/tests/`)

### `article.spec.ts`
Covers: F6 Create, F7 Edit, F8 Delete

| ID | Group | Test case | Tags | Known defect |
|---|---|---|---|---|
| UI-001 | Article (created through the API) | an article created via the API can be opened and shows its title |  |  |
| UI-002 | Article management (through the UI) | an author can create an article in the editor | @smoke |  |
| UI-003 | Article management (through the UI) | publishing without a title shows an error and stays on the editor |  |  |
| UI-004 | Article management (through the UI) | an author can edit an article | @smoke |  |
| UI-005 | Article management (through the UI) | an author can delete an article | @smoke |  |
| UI-006 | Article management (through the UI) | a visitor who is not the author cannot see edit or delete |  |  |

### `auth.spec.ts`
Covers: F1 Register, F2 Login

| ID | Group | Test case | Tags | Known defect |
|---|---|---|---|---|
| UI-007 | Authentication | login page renders the sign-in form |  |  |
| UI-008 | Authentication | login with invalid credentials shows an error |  |  |
| UI-009 | Authentication | a new user can register and is signed in |  |  |

### `comments.spec.ts`
Covers: F14 Comments

| ID | Group | Test case | Tags | Known defect |
|---|---|---|---|---|
| UI-010 | Comments | a signed-in user can post a comment | @smoke |  |
| UI-011 | Comments | an empty comment is rejected |  |  |
| UI-012 | Comments | a user can delete their own comment |  |  |
| UI-013 | Comments | a deleted comment stays gone after a reload |  | [BUG-007](bugs/BUG-007.md) |
| UI-014 | Comments | other users' comments are listed without a delete control |  |  |
| UI-015 | Comments | a signed-out visitor sees a sign-in prompt instead of the comment box |  |  |

### `favorites.spec.ts`
Covers: F12 Favorites

| ID | Group | Test case | Tags | Known defect |
|---|---|---|---|---|
| UI-016 | Favorites | a signed-in user can favorite and unfavorite an article | @smoke |  |
| UI-017 | Favorites | a favorite survives a reload |  |  |
| UI-018 | Favorites | a favorited article is listed under Favorited Articles on the profile |  |  |
| UI-019 | Favorites | a signed-out visitor who clicks favorite is sent to the login page |  |  |

### `feed.spec.ts`
Covers: F9 Feed and pagination, F10 Filters

| ID | Group | Test case | Tags | Known defect |
|---|---|---|---|---|
| UI-020 | Feeds | the global feed page loads with its tab | @smoke |  |
| UI-021 | Feeds | an article shows up in the feed filtered by its tag |  |  |
| UI-022 | Feeds | a tag with no articles shows the empty message |  |  |
| UI-023 | Feeds | a long feed shows 10 articles per page and a pager |  |  |
| UI-024 | Feeds | page 2 of a long feed shows the remaining article |  | [BUG-001](bugs/BUG-001.md) |

### `follow.spec.ts`
Covers: F11 Following feed, F13 Follow, F16 Profiles

| ID | Group | Test case | Tags | Known defect |
|---|---|---|---|---|
| UI-025 | Follow and the following feed | a user can follow and unfollow an author from the profile page | @smoke |  |
| UI-026 | Follow and the following feed | a user can follow and unfollow an author from the article page |  | [BUG-003](bugs/BUG-003.md) |
| UI-027 | Follow and the following feed | following survives a reload |  |  |
| UI-028 | Follow and the following feed | Your Feed is empty until you follow someone |  |  |
| UI-029 | Follow and the following feed | Your Feed shows articles from followed authors | @smoke |  |
| UI-030 | Follow and the following feed | a signed-out visitor who clicks follow is sent to the login page |  |  |
| UI-031 | Follow and the following feed | an author's profile lists that author's articles |  |  |

### `route-guards.spec.ts`
Covers: F4 Route guards

| ID | Group | Test case | Tags | Known defect |
|---|---|---|---|---|
| UI-032 | Route guards (signed out) | /settings redirects a signed-out visitor to the login page |  |  |
| UI-033 | Route guards (signed out) | /editor redirects a signed-out visitor to the login page |  |  |
| UI-034 | Route guards (signed out) | /editor/some-article redirects a signed-out visitor to the login page |  |  |
| UI-035 | Route guards (signed out) | /?feed=following redirects a signed-out visitor to the login page |  |  |
| UI-036 | Route guards (signed out) | the home page and article pages stay public |  |  |

### `session.spec.ts`
Covers: F3 Logout and session

| ID | Group | Test case | Tags | Known defect |
|---|---|---|---|---|
| UI-037 | Signed-in session (set up through the API) | a user created via the API is signed in without using the login form |  |  |
| UI-038 | Signed-in session (set up through the API) | a signed-in user can open the settings page |  |  |
| UI-039 | Signed-in session (set up through the API) | the token is planted only once, so a reload after logout stays signed out |  |  |
| UI-040 | Signed-in session (set up through the API) | a session survives a page reload | @smoke |  |
| UI-041 | Signed-in session (set up through the API) | logging out clears the session | @smoke |  |

### `settings.spec.ts`
Covers: F5 Settings

| ID | Group | Test case | Tags | Known defect |
|---|---|---|---|---|
| UI-042 | User settings | updating the bio saves it and opens the profile | @smoke |  |
| UI-043 | User settings | a changed password is accepted at the next login |  |  |
| UI-044 | User settings | changing the email to one that is already taken is rejected |  |  |
| UI-045 | User settings | settings can be saved with an empty image |  | [BUG-002](bugs/BUG-002.md) |

### `xss.spec.ts`
Covers: F17 Markdown and XSS

| ID | Group | Test case | Tags | Known defect |
|---|---|---|---|---|
| UI-046 | Markdown rendering is sanitised (XSS) | script, event handlers and javascript: links in the body are neutralised |  |  |

## API tests (pytest, `api-tests/tests/`)

### `test_articles.py`
Covers: F6-F10 Articles, feeds and filters, F15 Tags

| ID | Group | Test case | Tags | Known defect |
|---|---|---|---|---|
| API-001 | Create Article | Create returns the article with defaults | @smoke |  |
| API-002 | Create Article | The slug is built from the title |  |  |
| API-003 | Create Article | A missing field is rejected (title) |  |  |
| API-004 | Create Article | A missing field is rejected (description) |  |  |
| API-005 | Create Article | A missing field is rejected (body) |  |  |
| API-006 | Create Article | A duplicate title is a conflict |  |  |
| API-007 | Create Article | Creating requires a token |  |  |
| API-008 | Read Article | Anyone can read an article |  |  |
| API-009 | Read Article | An unknown slug is not found |  |  |
| API-010 | Update And Delete | The author can update an article | @smoke |  |
| API-011 | Update And Delete | The author can delete an article | @smoke |  |
| API-012 | List Articles | The list has articles and a count |  |  |
| API-013 | List Articles | Limit caps the page size |  |  |
| API-014 | List Articles | Filter by author |  |  |
| API-015 | List Articles | Filter by tag |  |  |
| API-016 | List Articles | Filter by favorited |  |  |
| API-017 | List Articles | A non numeric limit is rejected |  |  |
| API-018 | List Articles | A negative limit is rejected |  | [BUG-006](bugs/BUG-006.md) |
| API-019 | List Articles | The second page has the remaining articles |  | [BUG-001](bugs/BUG-001.md) |
| API-020 | Feed | The feed requires a token |  |  |
| API-021 | Feed | A new user has an empty feed |  |  |
| API-022 | Feed | The feed shows articles from followed authors only | @smoke |  |
| API-023 | Tags | A created tag appears in the tag list |  |  |
| API-024 | Soft Delete Is Hidden By The Api | The tags of a deleted article leave the tag list |  |  |
| API-025 | Soft Delete Is Hidden By The Api | The comments of a deleted article are not reachable |  |  |

### `test_authorization.py`
Covers: F4 Auth guards, F7/F8 author-only changes

| ID | Group | Test case | Tags | Known defect |
|---|---|---|---|---|
| API-026 | Other Users Cannot Chang Your Content | Another user cannot update an article |  |  |
| API-027 | Other Users Cannot Chang Your Content | Another user cannot delete an article |  |  |
| API-028 | Other Users Cannot Chang Your Content | Another user cannot delete a comment |  |  |
| API-029 |  | Endpoints that change data require a token (POST /articles) |  |  |
| API-030 |  | Endpoints that change data require a token (PUT /articles/{slug}) |  |  |
| API-031 |  | Endpoints that change data require a token (DELETE /articles/{slug}) |  |  |
| API-032 |  | Endpoints that change data require a token (GET /articles/feed) |  |  |
| API-033 |  | Endpoints that change data require a token (POST /articles/{slug}/favorite) |  |  |
| API-034 |  | Endpoints that change data require a token (DELETE /articles/{slug}/favorite) |  |  |
| API-035 |  | Endpoints that change data require a token (POST /articles/{slug}/comments) |  |  |
| API-036 |  | Endpoints that change data require a token (DELETE /articles/{slug}/comments/some-id) |  |  |
| API-037 |  | Endpoints that change data require a token (POST /profiles/{username}/follow) |  |  |
| API-038 |  | Endpoints that change data require a token (DELETE /profiles/{username}/follow) |  |  |
| API-039 |  | Endpoints that change data require a token (GET /user) |  |  |
| API-040 |  | Endpoints that change data require a token (PUT /user) |  |  |

### `test_comments.py`
Covers: F14 Comments

| ID | Group | Test case | Tags | Known defect |
|---|---|---|---|---|
| API-041 | Comments | A user can comment and it is listed | @smoke |  |
| API-042 | Comments | Comments are public to read |  |  |
| API-043 | Comments | An empty comment is rejected |  |  |
| API-044 | Comments | Commenting on an unknown article is not found |  |  |
| API-045 | Comments | The author can delete their comment | @smoke |  |
| API-046 | Comments | A deleted comment is gone from the list |  | [BUG-007](bugs/BUG-007.md) |

### `test_favorites.py`
Covers: F12 Favorites

| ID | Group | Test case | Tags | Known defect |
|---|---|---|---|---|
| API-047 | Favorites | Favoriting marks the article and counts it | @smoke |  |
| API-048 | Favorites | The count adds up across users |  |  |
| API-049 | Favorites | An anonymous reader sees the count |  |  |
| API-050 | Favorites | An anonymous reader does not see favorited |  | [BUG-008](bugs/BUG-008.md) |
| API-051 | Favorites | A user who did not favorite does not see favorited |  | [BUG-008](bugs/BUG-008.md) |
| API-052 | Favorites | Unfavoriting reverses it |  |  |
| API-053 | Favorites | Favoriting twice is rejected |  |  |
| API-054 | Favorites | Unfavoriting something not favorited is rejected |  |  |
| API-055 | Favorites | An unknown article is not found |  |  |

### `test_health.py`
Covers: Service health

| ID | Group | Test case | Tags | Known defect |
|---|---|---|---|---|
| API-056 |  | The health check is up | @smoke |  |

### `test_profiles.py`
Covers: F13 Follow, F16 Profiles

| ID | Group | Test case | Tags | Known defect |
|---|---|---|---|---|
| API-057 | Profiles | A profile is public |  |  |
| API-058 | Profiles | An unknown profile is not found |  |  |
| API-059 | Follow | Following is visible to the follower only | @smoke |  |
| API-060 | Follow | A user who does not follow sees following false |  |  |
| API-061 | Follow | An anonymous visitor does not see following |  | [BUG-009](bugs/BUG-009.md) |
| API-062 | Follow | Unfollowing reverses it |  |  |
| API-063 | Follow | You cannot follow yourself |  |  |
| API-064 | Follow | Following twice is rejected |  |  |
| API-065 | Follow | Following an unknown user is not found |  |  |

### `test_users.py`
Covers: F1 Register, F2 Login, F5 Settings

| ID | Group | Test case | Tags | Known defect |
|---|---|---|---|---|
| API-066 | Registration | Register returns the new user with a token | @smoke |  |
| API-067 | Registration | A duplicate username or email is a conflict (username) |  |  |
| API-068 | Registration | A duplicate username or email is a conflict (email) |  |  |
| API-069 | Registration | A missing field is rejected (username) |  |  |
| API-070 | Registration | A missing field is rejected (email) |  |  |
| API-071 | Registration | A missing field is rejected (password) |  |  |
| API-072 | Registration | An empty body is rejected |  |  |
| API-073 | Registration | A weak password is rejected |  |  |
| API-074 | Registration | An invalid email is rejected |  | [BUG-005](bugs/BUG-005.md) |
| API-075 | Login | Login returns a token that works | @smoke |  |
| API-076 | Login | A wrong password is unauthorized |  |  |
| API-077 | Login | An unknown email is not found |  |  |
| API-078 | Login | A missing password is rejected |  |  |
| API-079 | Current User | Get current user |  |  |
| API-080 | Current User | No token is unauthorized |  |  |
| API-081 | Current User | A garbage token is unauthorized |  |  |
| API-082 | Current User | The token scheme must be bearer |  |  |
| API-083 | Update User | Update the bio |  |  |
| API-084 | Update User | A new password works and the old one does not |  |  |
| API-085 | Update User | An invalid email is rejected |  |  |
| API-086 | Update User | A short password is rejected |  |  |
| API-087 | Update User | A taken email is a conflict |  | [BUG-004](bugs/BUG-004.md) |
| API-088 | Update User | A taken username is a conflict |  | [BUG-004](bugs/BUG-004.md) |
| API-089 | Update User | An empty bio can be saved |  | [BUG-002](bugs/BUG-002.md) |
