using Flurl;
using Flurl.Http;

namespace CourterClient.ApiClient;

internal class DefaultPublicClient : IPublicClient
{
    private readonly ResourceGetter _getter;

    public DefaultPublicClient(string routeUrl)
    {
        _getter = new ResourceGetter(routeUrl);
    }

    public async Task<ApiResponse<IEnumerable<CourtOut>>> GetCourtsAsync()
    {
        return await _getter.GetCollectionAsync<CourtOut>("courts").ConfigureAwait(false);
    }

    public async Task<ApiResponse<IEnumerable<TimeslotOut>>> GetTimeslotsAsync()
    {
        return await _getter.GetCollectionAsync<TimeslotOut>("timeslots").ConfigureAwait(false);
    }
}


