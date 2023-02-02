using Flurl;
using CourterClient.ApiClient;



var rootClient = new RootClient("http://localhost:8000");

var response = await rootClient.Login(new Credentials("customer100", "test1234"));
var customerClient = rootClient.MakeAccountClient();

var info = await customerClient.GetInfoAsync();
var newUsername = await customerClient.ChangeUsernameAsync("KäptnBlaubär");
var info2 = await customerClient.GetInfoAsync();

Console.ReadKey();

