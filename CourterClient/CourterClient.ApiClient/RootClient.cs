using System.Net;
using System.IdentityModel.Tokens.Jwt;
using Flurl;
using Flurl.Http;
using System.Security.Cryptography;

namespace CourterClient.ApiClient;

public class RootClient
{
    // TODO: move this elsewhere?
    private const string _dateFormat = "yyyy-MM-dd";

    private readonly string _apiUrl;
    private readonly ResourceAdder _adder;
    private Token? _token;
    private UserRole? _role;

    public RootClient(string apiUrl)
    {
        _apiUrl = apiUrl;
        _adder = new ResourceAdder(apiUrl);
    }

    public string Url { get { return _apiUrl; } }

    public async Task<ApiValueResponse<UserRole>> Login(Credentials credentials)
    {
        try
        {
            IFlurlResponse response = await _apiUrl.AppendPathSegment("token")
            .PostUrlEncodedAsync(new
            {
                username = credentials.Username,
                password = credentials.Password
            })
            .ConfigureAwait(false);

            _token = await response.GetJsonAsync<Token>().ConfigureAwait(false);
            ExtractRoleFromToken();

            return await ApiValueResponse<UserRole>.MakeSuccessful(response, _role).ConfigureAwait(false);
        }
        catch (FlurlHttpException exc)
        {
            return await ApiValueResponse<UserRole>.MakeUnsuccessful(exc).ConfigureAwait(false);
        }
    }

    public async Task<ApiResponse<UserOut>> SignUp(Credentials credentials)
    {
        return await _adder.AddAsync<UserOut, Credentials>("signup", credentials).ConfigureAwait(false);
    }

    public IPublicClient MakePublicClient()
    {
        return new DefaultPublicClient(_apiUrl.AppendPathSegment("public"));
    }

    public IAccountClient MakeAccountClient()
    {
        CheckLogin();
        return new DefaultAccountClient(_apiUrl.AppendPathSegment("account"), _token!.AccessToken);
    }

    public IAdminClient MakeAdminClient()
    {
        CheckLogin();
        CheckRole(UserRole.Admin);
        var adminClient = new DefaultAdminClient(_apiUrl.AppendPathSegment("admin"), _token!.AccessToken);
        return adminClient;
    }

    public IEmployeeClient MakeEmployeeClient()
    {
        CheckLogin();
        CheckRole(UserRole.Employee);
        var employeeClient = new DefaultEmployeeClient(
            _apiUrl.AppendPathSegment("employee"), _token!.AccessToken, _dateFormat);
        return employeeClient;
    }

    public ICustomerClient MakeCustomerClient()
    {
        CheckLogin();
        CheckRole(UserRole.Customer);
        var customerClient = new DefaultCustomerClient(
            _apiUrl.AppendPathSegment("customer"), _token!.AccessToken, _dateFormat);
        return customerClient;
    }

    private void CheckLogin()
    {
        if (_token is null)
            throw new LoginRequiredException();
    }

    private void CheckRole(UserRole requiredRole)
    {
        if (_role is null || _role != requiredRole)
        {
            string currentRole = _role is null ? "null" : _role.Value.ToString();
            throw new UserRoleException($"requires {requiredRole} role, current role is {currentRole}");
        }
    }

    private void ExtractRoleFromToken()
    {
        var handler = new JwtSecurityTokenHandler();
        var jwt = handler.ReadJwtToken(_token!.AccessToken);

        foreach (var claim in jwt.Claims)
        {
            if (claim.Type == "role")
            {
                switch (claim.Value)
                {
                    case "admin": _role = UserRole.Admin; break;
                    case "employee": _role = UserRole.Employee; break;
                    case "customer": _role = UserRole.Customer; break;
                }
                return;
            }
        }

        throw new UserRoleException("invalid or no user role");
    }
}

