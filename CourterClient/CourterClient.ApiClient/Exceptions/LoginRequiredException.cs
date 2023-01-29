using System;
namespace CourterClient.ApiClient;

public class LoginRequiredException : Exception
{
	public LoginRequiredException()
	{ }

	public LoginRequiredException(string message)
		: base(message)
	{ }
}

