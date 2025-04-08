# Linear SDK Capabilities Overview

The Linear TypeScript SDK provides a strongly typed interface to the Linear GraphQL API, allowing developers to build integrations and tools for Linear, the issue tracking platform.

## Core Features

- **TypeScript Support**: Full type definitions for all operations and models
- **Authentication**: Supports both API key and OAuth 2.0 authentication
- **Strongly Typed Models**: Exposes Linear's GraphQL schema through typed models

## Data Operations

### Querying Data
```typescript
// Get user data
const me = await linearClient.viewer;

// Fetch collections
const issues = await linearClient.issues();
const teams = await linearClient.teams();

// Get specific resources
const user = await linearClient.user("user-id");
const team = await linearClient.team("team-id");

// Filter and customize queries
const fiftyProjects = await linearClient.projects({ first: 50 });
const allComments = await linearClient.comments({ includeArchived: true });

// Chain operations
const me = await linearClient.viewer;
const myIssues = await me.assignedIssues();
const firstIssue = myIssues.nodes[0];
```

### Mutations (Create/Update/Delete)
```typescript
// Create resources
await linearClient.createIssue({ teamId: "team-id", title: "My Issue" });

// Update resources
await linearClient.updateUser("user-id", { displayName: "Alice" });
// Or from the model:
await user.update({ displayName: "Alice" });

// Delete/archive resources
await linearClient.archiveProject("project-id");
// Or from the model:
await project.archive();
```

### Pagination
```typescript
// Fetch pages with cursor-based pagination
const issues = await linearClient.issues({ after: "cursor", first: 10 });
const nextIssues = await issues.fetchNext();
const prevIssues = await issues.fetchPrevious();

// Access pagination info
const hasMoreIssues = issues.pageInfo.hasNextPage;
const issuesEndCursor = issues.pageInfo.endCursor;

// Ordering results
const issues = await linearClient.issues({ 
  orderBy: LinearDocument.PaginationOrderBy.UpdatedAt 
});
```

## Advanced Features

### Error Handling
```typescript
try {
  const result = await linearClient.createComment(input);
  return result.comment;
} catch (error) {
  if (error instanceof InvalidInputLinearError) {
    // Handle validation errors
  }
  // Access error details
  console.error("Failed query:", error.query);
  console.error("With variables:", error.variables);
  throw error;
}
```

### Webhooks
```typescript
import { LinearWebhooks, LINEAR_WEBHOOK_SIGNATURE_HEADER } from '@linear/sdk'

const webhook = new LinearWebhooks("WEBHOOK_SECRET");
// Use it to verify webhook signatures in your handler
```

### Raw GraphQL Access
```typescript
const graphQLClient = linearClient.client;
const result = await graphQLClient.rawRequest(`
  query cycle($id: String!) {
    cycle(id: $id) {
      id
      name
    }
  }`,
  { id: "cycle-id" }
);
```

### Custom GraphQL Client
The SDK allows for extending with custom GraphQL clients when needed.

## Resources

- [Linear API Documentation](https://developers.linear.app/docs)
- [SDK Source Code on GitHub](https://github.com/linear/linear/tree/master/packages/sdk) 