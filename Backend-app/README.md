[Walkthrough](https://www.loom.com/share/87eacfda7e9441c1b75cc7d71b6fc3d9?sid=cf1c26a0-6ca1-45ec-a629-7599253bef50)

## Usage
```bash
python -m app.app
```

### First time run
```bash
python init.py
```

### ENV
Provide these in .env file

**Mandatory**
-  `DATABASE_URL`: Postgres database connection string
-  `OPENAI_API_KEY`

**For tool use**
-  `EMAIL`: Email address for tools
-  `GOOGLE_APPLICATION_CREDENTIALS`: Path to credential file
-  `OPENPHONE_API_KEY`
-  `SHOPIFY_ACCESS_TOKEN`
-  `SHOPIFY_STORE`: Subdomain of the store

**Tracking**
- `LANGCHAIN_API_KEY`
- `LANGCHAIN_TRACING_V2=true`
- `LANGCHAIN_ENDPOINT=https://api.smith.langchain.com`
