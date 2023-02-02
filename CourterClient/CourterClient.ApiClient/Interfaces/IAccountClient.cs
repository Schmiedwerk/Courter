using System;
namespace CourterClient.ApiClient;

public interface IAccountClient
{
    Task<ApiResponse<UserOut>> GetInfoAsync();
    Task<ApiResponse> DeleteAccountAsync();
    Task<ApiResponse<UserOut>> ChangeUsernameAsync(string newUsername);
    Task<ApiResponse<UserOut>> ChangePasswordAsync(string newPassword);
}
