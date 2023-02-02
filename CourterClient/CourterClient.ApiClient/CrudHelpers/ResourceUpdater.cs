using Flurl;
using Flurl.Http;

namespace CourterClient.ApiClient;

internal class ResourceUpdater
{
	private readonly string _routeUrl;
	private readonly string? _accessToken;

	internal ResourceUpdater(string routeUrl, string? accessToken = null)
	{
		_routeUrl = routeUrl;
		_accessToken = accessToken;
	}

	internal async Task<ApiResponse<T>> UpdateWithQueryAsync<T, U>(string resourceSubroute, string queryKey, U queryValue)
		where T : class
	{
		Url queryUrl = _routeUrl.AppendPathSegment(resourceSubroute).SetQueryParam(queryKey, queryValue);

		try
		{
			IFlurlResponse response;

			if (_accessToken is null)
			{
				response = await queryUrl.PutAsync().ConfigureAwait(false);
			}
			else
			{
				response = await queryUrl.WithOAuthBearerToken(_accessToken)
					.PutAsync().ConfigureAwait(false);
			}

			return await ApiResponse<T>.MakeSuccessful(response).ConfigureAwait(false);
		}
		catch (FlurlHttpException exc)
		{
			return await ApiResponse<T>.MakeUnsuccessful(exc).ConfigureAwait(false);
		}
	}
}

