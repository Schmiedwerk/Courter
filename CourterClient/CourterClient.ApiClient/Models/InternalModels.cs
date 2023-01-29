namespace CourterClient.ApiClient;

internal record TokenResponse
{
    internal string? Access_Token { get; init; }
    internal string? Token_Type { get; init; }
}

internal record DetailResponse
{
    internal string? Detail { get; init; } 
}