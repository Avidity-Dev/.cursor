# Advanced Usage with Linear SDK

The Linear Client wraps the Linear SDK, provides a LinearGraphQLClient, and parses errors.

## Request Configuration

The `LinearGraphQLClient` can be configured by passing the `RequestInit` object to the Linear Client constructor:

```typescript
const linearClient = new LinearClient({ apiKey, headers: { "my-header": "value" } });
```

## Raw GraphQL Client

The `LinearGraphQLClient` is accessible through the Linear Client:

```typescript
const graphQLClient = linearClient.client;
graphQLClient.setHeader("my-header", "value");
```

## Raw GraphQL Queries

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

## Custom GraphQL Client

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