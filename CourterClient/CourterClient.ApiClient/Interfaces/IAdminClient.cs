using System;
namespace CourterClient.ApiClient;

public interface IAdminClient
{
    Task<ApiResponse<IEnumerable<UserOut>>> GetAdminsAsync();
    Task<ApiResponse<UserOut>> AddAdminAsync(Credentials credentials);
    Task<ApiResponse> DeleteAdminAsync(int id);

    Task<ApiResponse<IEnumerable<UserOut>>> GetEmployeesAsync();
    Task<ApiResponse<UserOut>> AddEmployeeAsync(Credentials credentials);
    Task<ApiResponse> DeleteEmployeeAsync(int id);

    Task<ApiResponse<CourtOut>> AddCourtAsync(CourtIn court);
    Task<ApiResponse> DeleteCourtAsync(int id);

    Task<ApiResponse<TimeslotOut>> AddTimeslotAsync(TimeslotIn timeslot);
    Task<ApiResponse> DeleteTimeslotAsync(int id);
}
