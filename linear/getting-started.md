# Getting Started with Linear SDK

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

## Connect to the Linear API and interact with your data in a few steps:

### 1. Install the Linear Client

Using npm:

```bash
npm install @linear/sdk
```

Or yarn:

```bash
yarn add @linear/sdk
```

### 2. Create a Linear client

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

### 3. Query for your issues

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