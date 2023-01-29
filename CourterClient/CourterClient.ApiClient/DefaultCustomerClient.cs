using System;
namespace CourterClient.ApiClient;

internal class DefaultCustomerClient : ICustomerClient
{
	private readonly TokenResponse _token;

	public DefaultCustomerClient(TokenResponse token)
	{
		_token = token;
	}
}

