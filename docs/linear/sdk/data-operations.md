# Fetching & Modifying Data with Linear SDK

## Queries

Some models can be fetched from the Linear Client without any arguments:

```typescript
const me = await linearClient.viewer;
const org = await linearClient.organization;
```

Other models are exposed as connections, and return a list of nodes:

```typescript
const issues = await linearClient.issues();
const firstIssue = issues.nodes[0];
```

All required variables are passed as the first arguments:

```typescript
const user = await linearClient.user("user-id");
const team = await linearClient.team("team-id");
```

Any optional variables are passed into the last argument as an object:

```typescript
const fiftyProjects = await linearClient.projects({ first: 50 });
const allComments = await linearClient.comments({ includeArchived: true });
```

Most models expose operations to fetch other models:

```typescript
const me = await linearClient.viewer;
const myIssues = await me.assignedIssues();
const myFirstIssue = myIssues.nodes[0];
const myFirstIssueComments = await myFirstIssue.comments();
const myFirstIssueFirstComment = myFirstIssueComments.nodes[0];
const myFirstIssueFirstCommentUser = await myFirstIssueFirstComment.user;
```

**NOTE:** Parenthesis is required only if the operation takes an optional variables object.

**TIP:** You can find ID's for any entity within the Linear app by searching for "Copy model UUID" in the command menu.

## Mutations

To create a model, call the Linear Client mutation and pass in the input object:

```typescript
const teams = await linearClient.teams();
const team = teams.nodes[0];
if (team.id) {
  await linearClient.createIssue({ teamId: team.id, title: "My Created Issue" });
}
```

To update a model, call the Linear Client mutation and pass in the required variables and input object:

```typescript
const me = await linearClient.viewer;
if (me.id) {
  await linearClient.updateUser(me.id, { displayName: "Alice" });
}
```

Or call the mutation from the model:

```typescript
const me = await linearClient.viewer;
await me.update({ displayName: "Alice" });
```

All mutations are exposed in the same way:

```typescript
const projects = await linearClient.projects();
const project = projects.nodes[0];
if (project.id) {
  await linearClient.archiveProject(project.id);
  await project.archive();
}
```

Mutations will often return a success boolean and the mutated entity:

```typescript
const commentPayload = await linearClient.createComment({ issueId: "some-issue-id" });
if (commentPayload.success) {
  return commentPayload.comment;
} else {
  return new Error("Failed to create comment");
}
```

## Pagination

Connection models have helpers to fetch the next and previous pages of results:

```typescript
const issues = await linearClient.issues({ after: "some-issue-cursor", first: 10 });
const nextIssues = await issues.fetchNext();
const prevIssues = await issues.fetchPrevious();
```

Pagination info is exposed and can be passed to the query operations. This uses the Relay Connection spec:

```typescript
const issues = await linearClient.issues();
const hasMoreIssues = issues.pageInfo.hasNextPage;
const issuesEndCursor = issues.pageInfo.endCursor;
const moreIssues = await linearClient.issues({ after: issuesEndCursor, first: 10 });
```

Results can be ordered using the `orderBy` optional variable:

```typescript
import { LinearDocument } from "@linear/sdk";

const issues = await linearClient.issues({ orderBy: LinearDocument.PaginationOrderBy.UpdatedAt });
```

Source: [Linear API Documentation - Fetching & Modifying Data](https://developers.linear.app/docs/sdk/fetching-and-modifying-data) 