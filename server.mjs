import { Provider } from 'oidc-provider';

const configuration = {
  clients: [{
    client_id: 'test-client',
    client_secret: 'test-secret',
    redirect_uris: ['http://localhost:5000/callback'],
    grant_types: ['authorization_code'],
    response_types: ['code'],
    token_endpoint_auth_method: 'client_secret_basic',
    scope: 'openid profile email'
  }],
  claims: {
    openid: ['sub'],
    email: ['email', 'email_verified'],
    profile: ['name']
  },
  scopes: ['openid', 'profile', 'email'],
  features: {
    devInteractions: { enabled: true },
    resourceIndicators: { enabled: true }
  },
  cookies: {
    keys: ['some-secure-key'],
  },
  jwks: {
    keys: [
      {
        kty: 'RSA',
        n: 'some-key',
        e: 'AQAB',
        d: 'some-private-key',
        p: 'some-prime1',
        q: 'some-prime2',
        dp: 'some-exponent1',
        dq: 'some-exponent2',
        qi: 'some-coefficient'
      }
    ]
  }
};

const provider = new Provider('http://localhost:3000', configuration);

provider.use(async (ctx, next) => {
  if (ctx.path === '/') {
    ctx.body = '<html><body><h1>OIDC Provider</h1><p>Server is running</p></body></html>';
  } else {
    await next();
  }
});

provider.listen(3000, () => {
  console.log('OIDC Provider listening on port 3000');
});