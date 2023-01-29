namespace CourterClient.ApiClient;

internal class DefaultAdminClient : IAdminClient
{
	private TokenResponse _token;

	public DefaultAdminClient(TokenResponse token)
	{
		_token = token;
	}
}

