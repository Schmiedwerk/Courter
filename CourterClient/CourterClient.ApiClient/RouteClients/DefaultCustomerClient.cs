using System;

namespace CourterClient.ApiClient;

internal class DefaultCustomerClient : ICustomerClient
{
    private const string _bookingSubroute = "bookings";

    private readonly string _dateFormat;
    private readonly ResourceGetter _getter;
    private readonly ResourceAdder _adder;
    private readonly ResourceDeleter _deleter;

	public DefaultCustomerClient(string routeUrl, string accessToken, string dateFormat)
	{
        _dateFormat = dateFormat;
        _getter = new ResourceGetter(routeUrl, accessToken);
        _adder = new ResourceAdder(routeUrl, accessToken);
        _deleter = new ResourceDeleter(routeUrl, accessToken);
	}

    public async Task<ApiResponse<IEnumerable<BookingOut>>> GetBookingsForDateAsync(DateOnly date)
    {
        return await _getter.GetCollectionAsync<BookingOut>(_bookingSubroute, date.ToString(_dateFormat))
            .ConfigureAwait(false);
    }

    public async Task<ApiResponse<BookingOut>> AddBookingAsync(CustomerBookingIn booking)
    {
        return await _adder.AddAsync<BookingOut, CustomerBookingIn>(_bookingSubroute, booking)
            .ConfigureAwait(false);
    }

    public async Task<ApiResponse> DeleteBookingAsync(int id)
    {
        return await _deleter.DeleteAsync(_bookingSubroute, id).ConfigureAwait(false);
    }
}

