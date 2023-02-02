using Flurl;
using Flurl.Http;

namespace CourterClient.ApiClient;

internal class ResourceDeleter
{
	private readonly string _routeUrl;
	private readonly string? _accessToken;

	internal ResourceDeleter(string routeUrl, string? accessToken = null)
	{
		_routeUrl = routeUrl;
		_accessToken = accessToken;
	}

	internal async Task<ApiResponse> DeleteAsync<U>(string resourceSubroute, U pathParam)
	{
		Url queryUrl = _routeUrl.AppendPathSegments(resourceSubroute, pathParam);
		try
		{
			IFlurlResponse response;

			if (_accessToken is null)
			{
				response = await queryUrl.DeleteAsync().ConfigureAwait(false);
			}
			else
			{
				response = await queryUrl.WithOAuthBearerToken(_accessToken)
					.DeleteAsync().ConfigureAwait(false);
			}

			return ApiResponse.MakeSuccessful(response);
		}
		catch (FlurlHttpException exc)
		{
			return await ApiResponse.MakeUnsuccessful(exc).ConfigureAwait(false);
		}
	}

    internal async Task<ApiResponse> DeleteAsync()
    {
        return await DeleteAsync("", "").ConfigureAwait(false);
    }
}

