using System;
using Newtonsoft.Json;

namespace CourterClient.ApiClient;

internal record Token(
    [property: JsonProperty("access_token")] string AccessToken,
    [property: JsonProperty("token_type")] string TokenType
);

internal record HttpExceptionBody(
    [property: JsonProperty("detail")] string? Detail
);
