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

internal record HttpValidationError(
    [property: JsonProperty("detail")] IList<ValidationError> Detail
);

internal record ValidationError(
    [property: JsonProperty("loc")] IList<string> Location,
    [property: JsonProperty("msg")] string Message,
    [property: JsonProperty("type")] string Type
);

