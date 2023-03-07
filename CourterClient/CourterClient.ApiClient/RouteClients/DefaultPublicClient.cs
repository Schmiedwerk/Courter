using Flurl;
using Flurl.Http;

namespace CourterClient.ApiClient;

internal class DefaultPublicClient : IPublicClient
{
    private readonly string _dateFormat;
    private readonly ResourceGetter _getter;

    public DefaultPublicClient(string routeUrl, string dateFormat)
    {
        _getter = new ResourceGetter(routeUrl);
        _dateFormat = dateFormat;
    }

    public async Task<ApiResponse<IEnumerable<CourtOut>>> GetCourtsAsync()
    {
        return await _getter.GetCollectionAsync<CourtOut>("courts").ConfigureAwait(false);
    }

    public async Task<ApiResponse<IEnumerable<TimeslotOut>>> GetTimeslotsAsync()
    {
        return await _getter.GetCollectionAsync<TimeslotOut>("timeslots").ConfigureAwait(false);
    }

    public async Task<ApiResponse<IEnumerable<ClosingOut>>> GetClosingsForDateAsync(DateOnly date)
    {
        return await _getter.GetCollectionAsync<ClosingOut>("closings", date.ToString(_dateFormat)).ConfigureAwait(false);
    }
}
