using System.Net;
using System.IdentityModel.Tokens.Jwt;
using Flurl;
using Flurl.Http;

namespace CourterClient.ApiClient;

public class RootClient
{
	private readonly Url _apiUrl;
	private TokenResponse? _accessToken;

	public RootClient(string apiUrl)
	{
		_apiUrl = apiUrl;
	}

	public string Url { get { return _apiUrl; } }

	public async Task<ApiResponse<UserRole>> Login(string username, string password)
	{
		try
		{
            TokenResponse accessToken = await _apiUrl
            .AppendPathSegment("/token")
            .PostUrlEncodedAsync(new
            {
                username,
                password
            })
            .ReceiveJson<TokenResponse>();

			var role = ExtractRoleFromToken(accessToken);
			_accessToken = accessToken;

			return new ApiResponse<UserRole>
			{
				Successful = true,
				Result = role
			};
        }
		catch (FlurlHttpException exc)
		{
			var detail = await exc.GetResponseJsonAsync<DetailResponse>();

			return new ApiResponse<UserRole>
			{
				Successful = false,
				StatusCode = exc.StatusCode,
				Detail = detail.Detail
			};
		}
    }

	public IAppClient CreateAppClient()
	{
		
		return new DefaultAppClient();
	}

	public IAdminClient CreateAdminClient()
	{
		CheckLoginSuccessful();
		return new DefaultAdminClient(_accessToken!);
	}

	public IEmployeeClient CreateEmployeeClient()
	{
		CheckLoginSuccessful();
		return new DefaultEmployeeClient(_accessToken!);
	}

	public ICustomerClient CreateCustomerClient()
	{
		CheckLoginSuccessful();
		return new DefaultCustomerClient(_accessToken!);

		
	}

	private void CheckLoginSuccessful()
	{
		if (_accessToken is null)
			throw new LoginRequiredException();
	}

	private static UserRole ExtractRoleFromToken(TokenResponse token)
	{
        var handler = new JwtSecurityTokenHandler();
        var jwt = handler.ReadJwtToken(token.Access_Token);

		foreach (var claim in jwt.Claims)
		{
			if (claim.Type == "role")
			{
				switch (claim.Value)
				{
                    case "admin": return UserRole.Admin;
                    case "employee": return UserRole.Employee;
                    case "customer": return UserRole.Customer;
                }
			}
		}

		throw new UserRoleException("invalid or no user role");
	}
}

