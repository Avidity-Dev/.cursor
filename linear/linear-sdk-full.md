# Linear SDK Capabilities Overview

The Linear TypeScript SDK provides a strongly typed interface to the Linear GraphQL API, allowing developers to build integrations and tools for Linear, the issue tracking platform.

# Table of Contents

1. [Linear SDK Capabilities Overview](#1-linear-sdk-capabilities-overview)
   - [1.1 Core Features](#11-core-features)
   - [1.2 Data Operations](#12-data-operations)
     - [1.2.1 Querying Data](#121-querying-data)
     - [1.2.2 Mutations (Create/Update/Delete)](#122-mutations-createupdatedelete)
     - [1.2.3 Pagination](#123-pagination)
   - [1.3 Advanced Features](#13-advanced-features)
     - [1.3.1 Error Handling](#131-error-handling)
     - [1.3.2 Webhooks](#132-webhooks)
     - [1.3.3 Raw GraphQL Access](#133-raw-graphql-access)
     - [1.3.4 Custom GraphQL Client](#134-custom-graphql-client)
   - [1.4 Resources](#14-resources)
2. [Getting Started with Linear SDK](#2-getting-started-with-linear-sdk)
   - [2.1 Connect to the Linear API](#21-connect-to-the-linear-api-and-interact-with-your-data-in-a-few-steps)
     - [2.1.1 Install the Linear Client](#211-install-the-linear-client)
     - [2.1.2 Create a Linear client](#212-create-a-linear-client)
     - [2.1.3 Query for your issues](#213-query-for-your-issues)
3. [Fetching & Modifying Data with Linear SDK](#3-fetching--modifying-data-with-linear-sdk)
   - [3.1 Queries](#31-queries)
   - [3.2 Mutations](#32-mutations)
   - [3.3 Pagination](#33-pagination)
4. [Error Handling in Linear SDK](#4-error-handling-in-linear-sdk)
5. [Advanced Usage with Linear SDK](#5-advanced-usage-with-linear-sdk)
   - [5.1 Request Configuration](#51-request-configuration)
   - [5.2 Raw GraphQL Client](#52-raw-graphql-client)
   - [5.3 Raw GraphQL Queries](#53-raw-graphql-queries)
   - [5.4 Custom GraphQL Client](#54-custom-graphql-client)
6. [Webhooks in Linear SDK](#6-webhooks-in-linear-sdk)
   - [6.1 Usage](#61-usage)
7. [Guides for Linear API](#7-guides-for-linear-api)
   - [7.1 How to Upload a File to Linear](#71-how-to-upload-a-file-to-linear)
   - [7.2 How to Create New Issues Using linear.new](#72-how-to-create-new-issues-using-linearnew)

---

# 1. Linear SDK Capabilities Overview

The Linear TypeScript SDK provides a strongly typed interface to the Linear GraphQL API, allowing developers to build integrations and tools for Linear, the issue tracking platform.

## 1.1 Core Features

- **TypeScript Support**: Full type definitions for all operations and models
- **Authentication**: Supports both API key and OAuth 2.0 authentication
- **Strongly Typed Models**: Exposes Linear's GraphQL schema through typed models

## 1.2 Data Operations

### 1.2.1 Querying Data
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

### 1.2.2 Mutations (Create/Update/Delete)
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

### 1.2.3 Pagination
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

## 1.3 Advanced Features

### 1.3.1 Error Handling
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

### 1.3.2 Webhooks
```typescript
import { LinearWebhooks, LINEAR_WEBHOOK_SIGNATURE_HEADER } from '@linear/sdk'

const webhook = new LinearWebhooks("WEBHOOK_SECRET");
// Use it to verify webhook signatures in your handler
```

### 1.3.3 Raw GraphQL Access
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

### 1.3.4 Custom GraphQL Client
The SDK allows for extending with custom GraphQL clients when needed.

## 1.4 Resources

- [Linear API Documentation](https://developers.linear.app/docs)
- [SDK Source Code on GitHub](https://github.com/linear/linear/tree/master/packages/sdk)


---


# 2. Getting Started with Linear SDK

The Linear Typescript SDK exposes the Linear GraphQL schema through strongly typed models and operations. It's written in Typescript but can also be used in any Javascript environment.

All operations return models, which can be used to perform operations for other models and all types are accessible through the Linear SDK package.

```typescript
import { LinearClient, LinearFetch, User } from "@linear/sdk";

const linearClient = new LinearClient({ apiKey });

async function getCurrentUser(): LinearFetch<User> {
  return linearClient.viewer;
}
```

You can view the Linear SDK source code on GitHub.

## 2.1 Connect to the Linear API and interact with your data in a few steps:

### 2.1.1 Install the Linear Client

Using npm:

```bash
npm install @linear/sdk
```

Or yarn:

```bash
yarn add @linear/sdk
```

### 2.1.2 Create a Linear client

SDK supports both authentication methods, personal API keys and OAuth 2. See authentication for more details. 

You can create a client after creating authentication keys:

```typescript
import { LinearClient } from '@linear/sdk'

// Api key authentication
const client1 = new LinearClient({
  apiKey: YOUR_PERSONAL_API_KEY
})

// OAuth2 authentication
const client2 = new LinearClient({
  accessToken: YOUR_OAUTH_ACCESS_TOKEN
})
```

### 2.1.3 Query for your issues

Using async await syntax:

```typescript
async function getMyIssues() {
  const me = await linearClient.viewer;
  const myIssues = await me.assignedIssues();

  if (myIssues.nodes.length) {
    myIssues.nodes.map(issue => console.log(`${me.displayName} has issue: ${issue.title}`));
  } else {
    console.log(`${me.displayName} has no issues`);
  }
}

getMyIssues();
```

Or promises:

```typescript
linearClient.viewer.then(me => {
  return me.assignedIssues().then(myIssues => {
    if (myIssues.nodes.length) {
      myIssues.nodes.map(issue => console.log(`${me.displayName} has issue: ${issue.title}`));
    } else {
      console.log(`${me.displayName} has no issues`);
    }
  });
});
```

Source: [Linear API Documentation - Getting Started](https://developers.linear.app/docs/sdk/getting-started)

---

# 3. Fetching & Modifying Data with Linear SDK

## 3.1 Queries

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

## 3.2 Mutations

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

## 3.3 Pagination

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

---

# 4. Error Handling in Linear SDK

Errors can be caught and interrogated by wrapping the operation in a try catch block:

```typescript
async function createComment(input: LinearDocument.CommentCreateInput): LinearFetch<Comment | UserError> {
  try {
    /** Try to create a comment */
    const commentPayload = await linearClient.createComment(input);
    /** Return it if available */
    return commentPayload.comment;
  } catch (error) {
    /** The error has been parsed by Linear Client */
    throw error;
  }
}
```

Or by catching the error thrown from a calling function:

```typescript
async function archiveFirstIssue(): LinearFetch<ArchivePayload> {
  const me = await linearClient.viewer;
  const issues = await me.assignedIssues();
  const firstIssue = issues.nodes[0];

  if (firstIssue?.id) {
    const payload = await linearClient.archiveIssue(firstIssue.id);
    return payload;
  } else {
    return undefined;
  }
}

archiveFirstIssue().catch(error => {
  throw error;
});
```

The parsed error type can be compared to determine the course of action:

```typescript
import { InvalidInputLinearError, LinearError, LinearErrorType } from '@linear/sdk'
import { UserError } from './custom-errors'

const input = { name: "Happy Team" };
createTeam(input).catch(error => {
  if (error instanceof InvalidInputLinearError) {
    /** If the mutation has failed due to an invalid user input return a custom user error */
    return new UserError(input, error);
  } else {
    /** Otherwise throw the error and handle in the calling function */
    throw error;
  }
});
```

Information about the `request` resulting in the error is attached if available:

```typescript
run().catch(error => {
  if (error instanceof LinearError) {
    console.error("Failed query:", error.query);
    console.error("With variables:", error.variables);
  }
  throw error;
});
```

Information about the `response` is attached if available:

```typescript
run().catch(error => {
  if (error instanceof LinearError) {
    console.error("Failed HTTP status:", error.status);
    console.error("Failed response data:", error.data);
  }
  throw error;
});
```

Any GraphQL `errors` are parsed and added to an array:

```typescript
run().catch(error => {
  if (error instanceof LinearError) {
    error.errors?.map(graphqlError => {
      console.log("Error message", graphqlError.message);
      console.log("LinearErrorType of this GraphQL error", graphqlError.type);
      console.log("Error due to user input", graphqlError.userError);
      console.log("Path through the GraphQL schema", graphqlError.path);
    });
  }
  throw error;
});
```

The `raw` error returned by the `LinearGraphQLClient` is still available:

```typescript
run().catch(error => {
  if (error instanceof LinearError) {
    console.log("The original error", error.raw);
  }
  throw error;
});
```

Source: [Linear API Documentation - Errors](https://developers.linear.app/docs/sdk/errors)

---

# 5. Advanced Usage with Linear SDK

The Linear Client wraps the Linear SDK, provides a LinearGraphQLClient, and parses errors.

## 5.1 Request Configuration

The `LinearGraphQLClient` can be configured by passing the `RequestInit` object to the Linear Client constructor:

```typescript
const linearClient = new LinearClient({ apiKey, headers: { "my-header": "value" } });
```

## 5.2 Raw GraphQL Client

The `LinearGraphQLClient` is accessible through the Linear Client:

```typescript
const graphQLClient = linearClient.client;
graphQLClient.setHeader("my-header", "value");
```

## 5.3 Raw GraphQL Queries

The Linear GraphQL API can be queried directly by passing a raw GraphQL query to the `LinearGraphQLClient`:

```typescript
const graphQLClient = linearClient.client;
const cycle = await graphQLClient.rawRequest(`
  query cycle($id: String!) {
    cycle(id: $id) {
      id
      name
      completedAt
    }
  }`,
  { id: "cycle-id" }
);
```

## 5.4 Custom GraphQL Client

In order to use a custom GraphQL Client, the Linear SDK must be extended and provided with a request function:

```typescript
import { LinearError, LinearFetch, LinearRequest, LinearSdk, parseLinearError, UserConnection } from "@linear/sdk";
import { DocumentNode, GraphQLClient, print } from "graphql";
import { CustomGraphqlClient } from "./graphql-client";

/** Create a custom client configured with the Linear API base url and API key */
const customGraphqlClient = new CustomGraphqlClient("https://api.linear.app/graphql", {
  headers: { Authorization: apiKey },
});

/** Create the custom request function */
const customLinearRequest: LinearRequest = <Response, Variables>(
  document: DocumentNode,
  variables?: Variables
) => {
  /** The request must take a GraphQL document and variables, then return a promise for the result */
  return customGraphqlClient.request<Data>(print(document), variables).catch(error => {
    /** Optionally catch and parse errors from the Linear API */
    throw parseLinearError(error);
  });
};

/** Extend the Linear SDK to provide a request function using the custom client */
class CustomLinearClient extends LinearSdk {
  public constructor() {
    super(customLinearRequest);
  }
}

/** Create an instance of the custom client */
const customLinearClient = new CustomLinearClient();

/** Use the custom client as if it were the Linear Client */
async function getUsers(): LinearFetch<UserConnection> {
  const users = await customLinearClient.users();
  return users;
}
```

Source: [Linear API Documentation - Advanced Usage](https://developers.linear.app/docs/sdk/advanced)

---

# 6. Webhooks in Linear SDK

The SDK provides a helper class to verify webhook signatures.

## 6.1 Usage

```typescript
import { LinearWebhooks, LINEAR_WEBHOOK_SIGNATURE_HEADER, LINEAR_WEBHOOK_TS_FIELD } from '@linear/sdk'

const webhook = new LinearWebhooks("WEBHOOK_SECRET");
...
// Use it in the webhook handler. Example with Express:
app.use('/hooks/linear',
    bodyParser.json({
      verify: (req, res, buf) => {
        webhook.verify(buf,
            req.headers[LINEAR_WEBHOOK_SIGNATURE_HEADER] as string,
            JSON.parse(buf.toString())[LINEAR_WEBHOOK_TS_FIELD]);
      }
    }),
    (req, res, next) => {
      //Handle the webhook event
      next()
    })
```

Source: [Linear API Documentation - Webhooks](https://developers.linear.app/docs/sdk/webhooks)

---

# 7. Guides for Linear API

## 7.1 How to Upload a File to Linear

This guide shows you how to upload a file to Linear while using the GraphQL API or TypeScript SDK.

Files uploaded to Linear are stored in Linear's private cloud storage. They are only intended to be used within Linear, and you must authenticate to access these files elsewhere.

### Include an Image or Video within Markdown Content

The easiest way to upload an image or a video to Linear's private cloud storage is to include a URL reference to it within markdown content that you provide while creating issues, comments, or documents.

For example, while using the `IssueCreate` mutation in the GraphQL API, include an image in the markdown content provided in the `description` field:

```graphql
mutation IssueCreate {
    issueCreate(
        input: {
            title: "Issue title"
            description: "Markdown image here: \n ![alt text](https://example.com/image.png)"
            teamId: "9cfb482a-81e3-4154-b5b9-2c805e70a02d"
        }
    ) {
        success
    }
}
```

The image file at `https://example.com/image.png` will be automatically uploaded to Linear's private cloud storage. You can also embed a base64 encoded image instead of a URL:

```
![alt text](data:image/jpeg;base64,...)
```

### Upload Files Manually

To upload directly to storage and for files other than images, use the `fileUpload` mutation to request a pre-signed upload URL, then send a `PUT` request to that URL with the file content.

Attempting to upload a file from the client-side will be blocked by Linear's Content Security Policy (CSP). You may request the signed upload URL from the client, but the `PUT` request must be executed on the server.

Here is an example using the TypeScript SDK to upload a file on the server:

```typescript
/** Uploads a file to Linear, returning the uploaded URL. @throws */
async function uploadFileToLinear(file: File): Promise<string> {
  const uploadPayload = await linearClient.fileUpload(file.type, file.name, file.size);

  if (!uploadPayload.success || !uploadPayload.uploadFile) {
    throw new Error("Failed to request upload URL");
  }

  const uploadUrl = uploadPayload.uploadFile.uploadUrl;
  const assetUrl = uploadPayload.uploadFile.assetUrl;

  // Make sure to copy the response headers for the PUT request
  const headers = new Headers();
  headers.set("Content-Type", file.type);
  headers.set("Cache-Control", "public, max-age=31536000");
  uploadPayload.uploadFile.headers.forEach(({ key, value }) => headers.set(key, value));

  try {
    await fetch(uploadUrl, {
      method: "PUT",
      headers,
      body: file
    });

    return assetUrl;
  } catch (e) {
    console.error(e);
    throw new Error("Failed to upload file to Linear");
  }
}
```

The resulting file URL now points to Linear's private cloud storage and can be used in API mutations, like creating an issue or a comment.

### Proxy the File Upload on the Server

If you're handling file uploads from a website, for example with the `<input type="file" />` element, you must forward the file to a server before attempting to upload it to Linear.

**Next.js Example**

Browse or run a full example that proxies a file upload through Next.js API Routes here: [https://github.com/linear/linear/tree/master/examples/nextjs-file-upload](https://github.com/linear/linear/tree/master/examples/nextjs-file-upload)

### Common Errors

- **CORS error when sending the `PUT` request**: You are trying to upload a file from the client-side rather than a server, which is not allowed. You must proxy the file upload request via a server.

- **403 Forbidden response from PUT request**: You likely forgot to copy the headers returned by the `fileUpload` mutation onto the `PUT` request. Note that the headers are returned in array format and must be transformed into an object or a `Headers` instance before including them in a `fetch` request.

Source: [Linear API Documentation - How to upload a file to Linear](https://developers.linear.app/docs/guides/how-to-upload-a-file-to-linear)

## 7.2 How to Create New Issues Using linear.new

You can open Linear using a link with specific query parameters to start issue creation and pre-fill fields. This is all available without needing to integrate with Linear API.

The following links trigger the creation of a new Linear issue in any browser and you can add query parameters after any of them to pre-fill issue fields:

* http://linear.app/new
* http://linear.app/team/<team ID>/new
* http://linear.new

For example, you can assign new issues to a specific person, set an estimate, add labels, or combine multiple parameters with instructions in the description to create a template for a user to fill out.

### Generate a Pre-filled Link

You can open any issue page in Linear, open command menu using `Cmd/Ctrl + K` and then select `_Copy pre-filled create issue URL to clipboard_`. This will copy the URL to the clipboard, allowing you to quickly create a URL with parameters that will pre-fill the new issue creation state with the same properties set on the issue page.

### Supported Parameters

#### `title` and `description`

Use to `+` indicate an empty space in the keyword. For example, `?title=My+Title` meaning "My Title".

Examples:

* `https://linear.new?title=My+issue+title&description=This+is+my+issue+description`
* `https://linear.app/team/LIN/new?title=Issues+with+scrolling+the+modal+window`

#### `status`

Indicates the initially selected status of the issue.

Can be set by `UUID` or name of the workflow status. When using `UUID` you also need to indicate a corresponding team key.

Examples:

* `https://linear.new?status=Todo`
* `https://linear.app/team/MOB/new?status=<UUID>`

#### `priority`

Indicates the initially selected priority of the issue.

Possible values are `high`, `urgent`, `medium` and `low`

Examples:

* `https://linear.new?priority=urgent`
* `https://linear.app/team/LIN/new?title=Important+Bug&priority=high`

#### `assignee`

Indicates the initially selected assignee of the issue.

Possible values: `UUID` of the specific user, display name (shortname) or a full name of a user

Examples:

* `https://linear.new?assignee=john`
* `https://linear.new?assignee=Erin+Baker`
* `https://linear.app/team/LIN/new?assignee=<UUID>`

#### `estimate`

Indicates the initially selected estimate of the issue. Applicable only when the targeted team has estimates feature enabled.

Can be set by their point number e.g. `estimate=4`

T-shirt sizes have the following point values: `No priority (0)`, `XS (1)`, `S(2)`, `M (3)`, `L (5)`, `XL (8)`, `XXL (13)`, `XXXL (21)`

Examples:

* `https://linear.app/team/LIN/new?estimate=2`

#### `cycle`

Indicates the initially selected cycle of the issue. Applicable only when the targeted team has cycles feature enabled.

Can be set by `UUID`, cycle number or a name of a cycle.

Examples:

* `https://linear.app/team/MOB?cycle=36`
* `https://linear.app/team/EU/new?cycle=focus+on+bugs`
* `https://linear.app/team/EU/new?cycle=<UUID>`

#### `label` or `labels`

Indicates the initially selected labels on the issue. If the label doesn't exist in the workspace, it will be ignored.

Examples:

* `https://linear.app/team/LIN/new?label=bug`
* `https://linear.new?labels=bug,android,comments`

#### `project`

Indicates the initially selected project in the issue. Requires `team` to be specified in the URL.

Can be set by `UUID` or the name of the project.

Examples:

* `https://linear.app/team/LIN/new?project=Project+page+improvements`
* `https://linear.app/team/MOB/new?project=<UUID>`

#### `project milestone`

Indicates the initially selected project milestones in the issue. Requires `team` and `project` to be specified in the URL.

Can be set by `UUID` or the name of the project milestone.

Examples:

* `https://linear.app/team/LIN/new?project=Project+page+improvements&projectMilestone=Beta`
* `https://linear.app/team/MOB/new?project=<UUID>&projectMilestone=<UUID>`

#### `template`

Indicates a template that will be used for the issue creation. Issue templates are a powerful tool to set multiple issue properties at once. Also, it's possible to specify sub-issues when using an issue template.

Can be set by `UUID` of the issue template.

Examples:

* `https://linear.app/team/LIN/new?template=<UUID>`

You can easily generate an issue template URL in the app. Go to your team's templates (under team settings), hover over the template you want to use, and then click the "Copy URL" action in the menu.

Source: [Linear API Documentation - How to create new issues using linear.new](https://developers.linear.app/docs/guides/how-to-create-new-issues-using-linear.new)