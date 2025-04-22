# Webhooks in Linear SDK

The SDK provides a helper class to verify webhook signatures.

## Usage

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