using System;
namespace CourterClient.ApiClient;

public interface IEmployeeClient
{
    Task<ApiResponse<IEnumerable<BookingOut>>> GetBookingsForDateAsync(DateOnly date);
    Task<ApiResponse<BookingOut>> AddGuestBookingAsync(GuestBookingIn booking);
    Task<ApiResponse> DeleteGuestBookingAsync(int id);

    Task<ApiResponse<IEnumerable<ClosingOut>>> GetClosingsForDateAsync(DateOnly date);
    Task<ApiResponse<ClosingOut>> AddClosingAsync(ClosingIn closing);
    Task<ApiResponse> DeleteClosingAsync(int id);
}
