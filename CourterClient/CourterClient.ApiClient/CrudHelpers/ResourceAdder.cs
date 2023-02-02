using Flurl;
using Flurl.Http;

namespace CourterClient.ApiClient;

internal class ResourceAdder
{
    private readonly string _routeUrl;
    private readonly string? _accessToken;

    internal ResourceAdder(string routeUrl, string? accessToken = null)
    {
        _routeUrl = routeUrl;
        _accessToken = accessToken;
    }

    internal async Task<ApiResponse<T>> AddAsync<T, U>(string resourceSubroute, U resourceIn)
        where T : class
    {
        Url queryUrl = _routeUrl.AppendPathSegment(resourceSubroute);

        try
        {
            IFlurlResponse response;

            if (_accessToken is null)
            {
                response = await queryUrl.PostJsonAsync(resourceIn).ConfigureAwait(false);
            }
            else
            {
                response = await queryUrl.WithOAuthBearerToken(_accessToken)
                    .PostJsonAsync(resourceIn).ConfigureAwait(false);
            }

            return await ApiResponse<T>.MakeSuccessful(response).ConfigureAwait(false);
        }
        catch (FlurlHttpException exc)
        {
            return await ApiResponse<T>.MakeUnsuccessful(exc).ConfigureAwait(false);
        }
    }
}
