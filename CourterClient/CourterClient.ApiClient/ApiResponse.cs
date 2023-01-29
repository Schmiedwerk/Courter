using System;
namespace CourterClient.ApiClient;

public record ApiResponse
{
    public bool Successful { get; init; }
    public int? StatusCode { get; init; }
    public string? Detail { get; init; }
}

public record ApiResponse<T> : ApiResponse
{
    public T? Result { get; init; }
}
