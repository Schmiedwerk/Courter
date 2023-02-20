using System.Net;
using Flurl.Http;

namespace CourterClient.ApiClient;

public class ApiResponse
{
    public bool Successful { get; protected init; }
    public int? StatusCode { get; protected init; }
    public string? Detail { get; protected init; }

    internal static ApiResponse MakeSuccessful(IFlurlResponse response)
    {
        return new ApiResponse
        {
            Successful = true,
            StatusCode = response.StatusCode,
            Detail = null
        };
    }

    internal static async Task<ApiResponse> MakeUnsuccessful(FlurlHttpException exc)
    {
        return new ApiResponse
        {
            Successful = false,
            StatusCode = exc.StatusCode,
            Detail = await ExtractDetail(exc)
        };
    }

    protected static async Task<string?> ExtractDetail(FlurlHttpException exc)
    {
        string? detail;

        if (exc.StatusCode == (int)HttpStatusCode.UnprocessableEntity)
        {
            HttpValidationError error = await exc.GetResponseJsonAsync<HttpValidationError>().ConfigureAwait(false);
            ValidationError valError = error.Detail[0];
            detail = $"{valError.Location[1]}: {valError.Message}";
        }
        else
        {
            HttpExceptionBody excBody = await exc.GetResponseJsonAsync<HttpExceptionBody>().ConfigureAwait(false);
            detail = excBody.Detail;
        }

        return detail;
    }
}

public class ApiResponse<T> : ApiResponse
    where T : class
{
    public T? Result { get; private init; }

    internal static async Task<ApiResponse<T>> MakeSuccessful(IFlurlResponse response, T? result = null)
    {
        result ??= await response.GetJsonAsync<T>().ConfigureAwait(false);

        return new ApiResponse<T>
        {
            Successful = true,
            StatusCode = response.StatusCode,
            Detail = null,
            Result = result
        };
    }

    new internal static async Task<ApiResponse<T>> MakeUnsuccessful(FlurlHttpException exc)
    {
        return new ApiResponse<T>
        {
            Successful = false,
            StatusCode = exc.StatusCode,
            Detail = await ExtractDetail(exc),
            Result = null
        };
    }
}

public class ApiValueResponse<T> : ApiResponse
    where T : struct
{
    public T? Result { get; private init; }

    internal static async Task<ApiValueResponse<T>> MakeSuccessful(IFlurlResponse response, T? result = null)
    {
        result ??= await response.GetJsonAsync<T>().ConfigureAwait(false);

        return new ApiValueResponse<T>
        {
            Successful = true,
            StatusCode = response.StatusCode,
            Detail = null,
            Result = result
        };
    }

    new internal static async Task<ApiValueResponse<T>> MakeUnsuccessful(FlurlHttpException exc)
    {
        return new ApiValueResponse<T>
        {
            Successful = false,
            StatusCode = exc.StatusCode,
            Detail = await ExtractDetail(exc),
            Result = null
        };
    }
}
