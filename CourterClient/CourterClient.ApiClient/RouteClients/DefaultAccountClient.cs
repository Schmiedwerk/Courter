using System;

namespace CourterClient.ApiClient;

internal class DefaultAccountClient : IAccountClient
{
    private readonly ResourceGetter _getter;
    private readonly ResourceUpdater _updater;
    private readonly ResourceDeleter _deleter;

	internal DefaultAccountClient(string routeUrl, string accessToken)
	{
        _getter = new ResourceGetter(routeUrl, accessToken);
        _updater = new ResourceUpdater(routeUrl, accessToken);
        _deleter = new ResourceDeleter(routeUrl, accessToken);
	}

    public async Task<ApiResponse<UserOut>> GetInfoAsync()
    {
        return await _getter.GetAsync<UserOut>().ConfigureAwait(false);
    }

    public async Task<ApiResponse> DeleteAccountAsync()
    {
        return await _deleter.DeleteAsync().ConfigureAwait(false);
    }

    public async Task<ApiResponse<UserOut>> ChangeUsernameAsync(string newUsername)
    {
        return await _updater
            .UpdateWithQueryAsync<UserOut, string>("username", "new_username", newUsername)
            .ConfigureAwait(false); 
    }

    public async Task<ApiResponse<UserOut>> ChangePasswordAsync(string newPassword)
    {
        return await _updater
            .UpdateWithQueryAsync<UserOut, string>("password", "new_password", newPassword)
            .ConfigureAwait(false);
    }
}

