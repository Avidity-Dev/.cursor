# How to Upload a File to Linear

This guide shows you how to upload a file to Linear while using the GraphQL API or TypeScript SDK.

Files uploaded to Linear are stored in Linear's private cloud storage. They are only intended to be used within Linear, and you must authenticate to access these files elsewhere.

## Include an Image or Video within Markdown Content

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

## Upload Files Manually

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

## Proxy the File Upload on the Server

If you're handling file uploads from a website, for example with the `<input type="file" />` element, you must forward the file to a server before attempting to upload it to Linear.

**Next.js Example**

Browse or run a full example that proxies a file upload through Next.js API Routes here: [https://github.com/linear/linear/tree/master/examples/nextjs-file-upload](https://github.com/linear/linear/tree/master/examples/nextjs-file-upload)

## Common Errors

- **CORS error when sending the `PUT` request**: You are trying to upload a file from the client-side rather than a server, which is not allowed. You must proxy the file upload request via a server.

- **403 Forbidden response from PUT request**: You likely forgot to copy the headers returned by the `fileUpload` mutation onto the `PUT` request. Note that the headers are returned in array format and must be transformed into an object or a `Headers` instance before including them in a `fetch` request.

Source: [Linear API Documentation - How to upload a file to Linear](https://developers.linear.app/docs/guides/how-to-upload-a-file-to-linear) 