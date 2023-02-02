using System;

namespace CourterClient.ApiClient;

public interface ICustomerClient
{
    Task<ApiResponse<IEnumerable<BookingOut>>> GetBookingsForDateAsync(DateOnly date);
    Task<ApiResponse<BookingOut>> AddBookingAsync(CustomerBookingIn booking);
    Task<ApiResponse> DeleteBookingAsync(int id);
}

