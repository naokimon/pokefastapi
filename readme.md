# PokeFastAPI

A REST API for accessing basic Pokémon data. Built with FastAPI, AIOSQLite, and SQLite.

![banner](src/banner.jpg)

---

## Base URL

When running locally:

```text
http://127.0.0.1:8000
```

## Endpoints

### `GET /`

Returns a simple API status message.

#### Response

```json
{
  "Root": "This is the root of the API."
}
```

---

## Rate Limiting

All API routes are limited to **2 requests per second per client IP address** using SlowAPI.

When the rate limit is exceeded, the API returns HTTP status `429 Too Many Requests`.

#### Response

```json
{
  "error": "Rate limit exceeded: 2 per 1 second"
}
```

---

### `GET /pokemon`

Returns a paginated list of Pokémon.

#### Query Parameters

| Parameter   | Type    | Default | Description                                      |
|-------------|---------|---------|--------------------------------------------------|
| `limit`     | integer | `20`    | Number of Pokémon to return. Must be greater than `0`. |
| `offset`    | integer | `0`     | Number of Pokémon to skip.                       |
| `sort`      | string  | —       | Sort Pokémon by any of their database fields.    |
| `direction` | string  | `ASC`   | Sorting direction: `ASC` or `DESC`.              |

#### Example

```http
GET /pokemon?limit=20&offset=0
```

#### Response

```json
{
  "count": 20,
  "next": "http://127.0.0.1:8000/pokemon?limit=20&offset=20",
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "Bulbasaur",
      "form": null,
      "gen": 1,
      "types": [
        {
          "slot": 1,
          "type": {
            "name": "Grass"
          }
        },
        {
          "slot": 2,
          "type": {
            "name": "Poison"
          }
        }
      ],
      "stats": [
        {
          "base_stat": 45,
          "stat": {
            "name": "hp"
          }
        }
      ]
    }
  ]
}
```

`next` contains the URL for the next page. `previous` is `null` when there is no previous page.

If `limit` is `0` or negative, the API returns:

```json
{
  "detail": "Limit must be greater then 0!"
}
```

with HTTP status `404`.

---

### `GET /pokemon/{identifier}`

Returns a single Pokémon by its ID or exact name.

#### Path Parameter

| Parameter    | Type   | Description         |
| ------------ | ------ | ------------------- |
| `identifier` | string | Pokémon ID or name. |

#### Examples

By ID:

```http
GET /pokemon/1
```

By name:

```http
GET /pokemon/Bulbasaur
```

#### Response

```json
{
  "id": 1,
  "name": "Bulbasaur",
  "form": null,
  "gen": 1,
  "types": [
    {
      "slot": 1,
      "type": {
        "name": "Grass"
      }
    },
    {
      "slot": 2,
      "type": {
        "name": "Poison"
      }
    }
  ],
  "stats": [
    {
      "base_stat": 45,
      "stat": {
        "name": "hp"
      }
    }
  ]
}
```

If the Pokémon does not exist, the API returns:

```json
{
  "detail": "Pokemon not found!"
}
```

with HTTP status `404`.

---

### `GET /debug`

Returns the client's IP address and forwarded IP headers. Useful for debugging IP detection when running behind a reverse proxy such as Railway.

This endpoint is also limited to **2 requests per second**.

#### Response

```json
{
  "client": "100.64.0.2",
  "forwarded_for": "195.169.184.44, 152.233.12.241",
  "real_ip": "195.169.184.44"
}
```

#### Response Fields

| Field           | Type          | Description                                                      |
| --------------- | ------------- | ---------------------------------------------------------------- |
| `client`        | string / null | Client IP address detected by FastAPI.                           |
| `forwarded_for` | string / null | Client and proxy IP addresses from the `X-Forwarded-For` header. |
| `real_ip`       | string / null | Client IP address from the `X-Real-IP` header.                   |

When running behind a reverse proxy, `client` may contain the proxy's internal IP address instead of the original client's IP. Forwarded IP headers may be `null` when running locally.

---


## Pokémon Object

A Pokémon object contains:

| Field       | Type          | Description                      |
|-------------|---------------|----------------------------------|
| `id`        | integer       | Pokémon ID.                      |
| `name`      | string        | Pokémon name.                    |
| `form`      | string / null | Pokémon form, if applicable.     |
| `gen`       | integer       | Pokémon generation.              |
| `image_uri` | string        | Pokémon's Official Artwork image |
| `types`     | array         | Pokémon's type(s).               |
| `stats`     | array         | Pokémon's base stats.            |

Each item in `types` contains a `slot` and a `type.name`.

Each item in `stats` contains a `base_stat` and a `stat.name`.

---

## HTTP Errors

| Status | Condition                             |
|--------|---------------------------------------|
| `400`  | `limit` is less than or equal to `0`. |
| `400`  | `offset` is less than `0`.            |
| `404`  | Pokémon was not found.                |
| `429`  | Too many requests.                    |

