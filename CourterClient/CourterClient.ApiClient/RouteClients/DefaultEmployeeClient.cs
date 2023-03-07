using System;

namespace CourterClient.ApiClient;

internal class DefaultEmployeeClient : IEmployeeClient
{
    private const string _bookingsSubroute = "bookings";
    private const string _closingsSubroute = "closings";

    private readonly string _dateFormat;
    private readonly ResourceGetter _getter;
    private readonly ResourceAdder _adder;
    private readonly ResourceDeleter _deleter;

	public DefaultEmployeeClient(string routeUrl, string accessToken, string dateFormat)
	{
        _getter = new ResourceGetter(routeUrl, accessToken);
        _adder = new ResourceAdder(routeUrl, accessToken);
        _deleter = new ResourceDeleter(routeUrl, accessToken);
        _dateFormat = dateFormat;
    }

    public async Task<ApiResponse<IEnumerable<BookingOut>>> GetBookingsForDateAsync(DateOnly date)
    {
        return await _getter.GetCollectionAsync<BookingOut>(_bookingsSubroute, date.ToString(_dateFormat)).ConfigureAwait(false);
    }

    public async Task<ApiResponse<BookingOut>> AddGuestBookingAsync(GuestBookingIn booking)
    {
        return await _adder.AddAsync<BookingOut, GuestBookingIn>(_bookingsSubroute, booking).ConfigureAwait(false);
    }

    public async Task<ApiResponse> DeleteGuestBookingAsync(int id)
    {
        return await _deleter.DeleteAsync(_bookingsSubroute, id).ConfigureAwait(false);
    }

    public async Task<ApiResponse<ClosingOut>> AddClosingAsync(ClosingIn closing)
    {
        return await _adder.AddAsync<ClosingOut, ClosingIn>(_closingsSubroute, closing).ConfigureAwait(false);
    }

    public async Task<ApiResponse> DeleteClosingAsync(int id)
    {
        return await _deleter.DeleteAsync(_closingsSubroute, id).ConfigureAwait(false);
    }
}

