using Flurl;
using Flurl.Http;

namespace CourterClient.ApiClient;

internal class DefaultAdminClient : IAdminClient
{
    private const string _adminsSubroute = "admins";
    private const string _employeesSubroute = "employees";
    private const string _courtsSubroute = "courts";
    private const string _timeslotsSubroute = "timeslots";

    private readonly ResourceGetter _getter;
    private readonly ResourceDeleter _deleter;
    private readonly ResourceAdder _adder;

	public DefaultAdminClient(string routeUrl, string accessToken)
	{
        _getter = new ResourceGetter(routeUrl, accessToken);
        _deleter = new ResourceDeleter(routeUrl, accessToken);
        _adder = new ResourceAdder(routeUrl, accessToken);
        
	}

    public async Task<ApiResponse<IEnumerable<UserOut>>> GetAdminsAsync()
    {
        return await _getter.GetCollectionAsync<UserOut>(_adminsSubroute).ConfigureAwait(false);
    }

    public async Task<ApiResponse<UserOut>> AddAdminAsync(Credentials credentials)
    {
        return await _adder.AddAsync<UserOut, Credentials>(_adminsSubroute, credentials).ConfigureAwait(false);
    }

    public async Task<ApiResponse> DeleteAdminAsync(int id)
    {
        return await _deleter.DeleteAsync(_adminsSubroute, id).ConfigureAwait(false);
    }

    public async Task<ApiResponse<IEnumerable<UserOut>>> GetEmployeesAsync()
    {
        return await _getter.GetCollectionAsync<UserOut>(_employeesSubroute).ConfigureAwait(false);
    }

    public async Task<ApiResponse<UserOut>> AddEmployeeAsync(Credentials credentials)
    {
        return await _adder.AddAsync<UserOut, Credentials>(_employeesSubroute, credentials).ConfigureAwait(false);
    }

    public async Task<ApiResponse> DeleteEmployeeAsync(int id)
    {
        return await _deleter.DeleteAsync(_employeesSubroute, id).ConfigureAwait(false);
    }

    public async Task<ApiResponse<CourtOut>> AddCourtAsync(CourtIn court)
    {
        return await _adder.AddAsync<CourtOut, CourtIn>(_courtsSubroute, court).ConfigureAwait(false);
    }

    public async Task<ApiResponse> DeleteCourtAsync(int id)
    {
        return await _deleter.DeleteAsync(_courtsSubroute, id).ConfigureAwait(false);
    }

    public async Task<ApiResponse<TimeslotOut>> AddTimeslotAsync(TimeslotIn timeslot)
    {
        return await _adder.AddAsync<TimeslotOut, TimeslotIn>(_timeslotsSubroute, timeslot).ConfigureAwait(false);
    }

    public async Task<ApiResponse> DeleteTimeslotAsync(int id)
    {
        return await _deleter.DeleteAsync(_timeslotsSubroute, id).ConfigureAwait(false);
    }   
}
