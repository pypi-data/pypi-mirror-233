# clearskies-akeyless-custom-producer

Contains clearskies handlers that should make it very easy to create custom producers for Akeyless.

There are a variety of ways to manage custom producers for Akeyless.  The strategy utilized in this library is aimed at creating a stateless set of producer endpoints.  This works because you can store a payload in the customer producer in Akeless, and then Akeyless will provide this to the custom producer endpoint when it calls them.  As a result, the custom producer endpoints make use of the data provided in the payload rather than storing any secrets themselves.  This dramatically simplifies management of the endpoints.  In addition, this removes the need to manage authentication and authorization.  The reason is because Akeyless will only call your endpoint and pass along the payload in the event that it received a properly authorized request.  Therefore, the payload will only be present for authorized users, and since the custom producer endpoints don't store any credentials on their own, they are incapable of fulfilling requests on their own without being called properly by Akeyless.

This assumes that the payload stored in the custom producer is in JSON format.  Note, however, that this is merely a convention of this library: Akeyless does nothing to enforce valid JSON in payloads, so you must ensure that your payloads are properly formatted yourself.

# Installation, Documentation, and Usage

To install:

```
pip3 install clear-skies-akeyless-custom-producer
```

# Default Mode

There are a few options for managing credentials.  The "default" mode involves passing along two methods: one to create new credentials and one to revoke new credentials.  Your methods will be called as necessary.  You can request any named dependency injection parameters as needed.  In addition, you can request the `payload` parameter in your function and will receive the full payload data as a dictionary, or you can specify individual keys from the payload.  Your create function then uses the given data to create a new credential and returns the details as a dictionary.

In order to support later rotation of credentials, Akeyless requires that you specify an id for the new credential.  The revoke function will be called and this id will be provided back so that you can revoke a credential when it should expire.  To support this, an additional parameter is provided to the revoke function.  On top of `payload` and the various properties of the payload, your delete function should also provide the `id_to_delete` parameter which will contain the id of the credential that must be deleted.

Here's an example where an API call is used to create/revoke a credential with two parameters: `key` (the id) and `secret`.

```
import clearskies
from clearskies_akeyless_custom_producer.handlers import NoInput
def create(key, secret, requests):
    return requests.post(
        'https://key-generator.example.com',
        headers={
            'x-api-key': key,
            'x-api-secret': secret,
        }
    ).json()

def revoke(key, secret, requests, id_to_delete):
    return requests.delete(
        'https://key-generator.example.com/' + id_to_delete,
        headers={
            'x-api-key': key,
            'x-api-secret': secret,
        }
    )

custom_producer = clearskies.application(
    NoInput,
    {
        "create_callable": create,
        "revoke_callable": revoke,
        "id_column_name": "key",
    }
)
```
and then you can just attach your application to the appropriate context and execute it:

```
wsgi = clearskies.contexts.wsgi(custom_producer)
def application(env, start_response):
    return wsgi(env, start_response)
```

This will generate three endpoints:

 1. `/sync/create`
 2. `/sync/revoke`
 3. `/sync/rotate`

Which are where you point the akeyless custom producer.  Note that for rotation, it will call your create endpoint to make a new credential and then use the new credential to call the revoke endpoint for the old credential.

# Alternate Modes

### No Revoke

Sometimes you may not be able to revoke a credential (for instance, if issuing JWTs).  You can then just turn off the revoke step by setting `"can_revoke": False` in the configuration.  Akeyless requires a revoke step, so it will still be published by the handler, but it won't take any action.  Finally, since there is no attempt to revoke credentials, it's not necessary to track credential ids, so `id_column_name` is no longer required in this case:

```
custom_producer = clearskies.application(
    NoInput,
    {
        "create_callable": create,
        "can_revoke": False,
    }
)
```

### Custom Rotation

In some cases rotation is as simple as generating a new credential in the "usual" way and deleting the old credential.  This is the "default" usage describe above, and so there is no need for an explicit rotation step.  However, in some cases there may be a separate process for rotation, in which case you can provide a `rotate_callable`:

```
def rotate(requests, key, secret):
    return requests.patch(
        'https://key-generator.example.com/',
        headers={
            'x-api-key': key,
            'x-api-secret': secret,
        }
    ).json()

custom_producer = clearskies.application(
    NoInput,
    {
        "create_callable": create,
        "rotate_callable": rotate,
        "revoke_callable": revoke,
        "id_column_name": "key",
    }
)
```

### No Rotation

Sometimes rotation simply isn't possible, in which case you can completely disable it:

```
custom_producer = clearskies.application(
    NoInput,
    {
        "create_callable": create,
        "revoke_callable": revoke,
        "can_rotate": False,
        "id_column_name": "key",
    }
)
```

# With Input

Akeyless provides an option for allowing the client to pass additional input to the custom produccer which it can use when issuing credentials.  It's important to be very careful when processing user input in these cases, to ensure that users can't arbitrarily adjust the permissions of the generated credentials.  Still, if you want to allow users to impact the credential generation process, you can do that using the `WithInput` handler (which doesn't exist yet).
