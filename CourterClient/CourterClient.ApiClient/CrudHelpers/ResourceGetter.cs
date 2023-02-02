using Flurl;
using Flurl.Http;

namespace CourterClient.ApiClient;

internal class ResourceGetter
{
	private readonly string _routeUrl;
	private readonly string? _accessToken;

	internal ResourceGetter(string routeUrl, string? accessToken = null)
	{
		_routeUrl = routeUrl;
		_accessToken = accessToken;
	}

	internal async Task<ApiResponse<T>> GetAsync<T>(string resourceSubroute = "", string pathParam = "")
		where T : class
	{
		try
		{
			IFlurlResponse response = await MakeGetRequest(resourceSubroute, pathParam).ConfigureAwait(false);

			return await ApiResponse<T>.MakeSuccessful(response).ConfigureAwait(false);
		}
		catch (FlurlHttpException exc)
		{
			return await ApiResponse<T>.MakeUnsuccessful(exc).ConfigureAwait(false);
		}
	}

	internal async Task<ApiResponse<IEnumerable<T>>> GetCollectionAsync<T>(string resourceSubroute = "", string pathParam = "")
	{
		try
		{
			IFlurlResponse response = await MakeGetRequest(resourceSubroute, pathParam).ConfigureAwait(false);

			return await ApiResponse<IEnumerable<T>>.MakeSuccessful(response).ConfigureAwait(false);
		}
		catch (FlurlHttpException exc)
		{
			return await ApiResponse<IEnumerable<T>>.MakeUnsuccessful(exc).ConfigureAwait(false);
		}
	}

	private async Task<IFlurlResponse> MakeGetRequest(string resourceSubroute, string pathParam)
	{
		Url queryUrl = _routeUrl.AppendPathSegments(resourceSubroute, pathParam);

		if (_accessToken is null)
		{
			return await queryUrl.GetAsync().ConfigureAwait(false);
		}

		return await queryUrl.WithOAuthBearerToken(_accessToken).GetAsync().ConfigureAwait(false);
	}	
}
