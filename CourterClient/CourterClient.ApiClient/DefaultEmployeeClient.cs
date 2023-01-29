using System;
namespace CourterClient.ApiClient;

internal class DefaultEmployeeClient : IEmployeeClient
{
	private readonly TokenResponse _token;

	public DefaultEmployeeClient(TokenResponse token)
	{
		_token = token;
	}
}

