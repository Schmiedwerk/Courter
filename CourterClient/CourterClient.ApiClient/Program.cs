using CourterClient.ApiClient;

var rootClient = new RootClient("http://localhost:8000");

var response = await rootClient.Login("root", "test12345");

Console.WriteLine(response.Successful);
Console.WriteLine(response.StatusCode);
Console.WriteLine(response.Detail);

Console.ReadKey();
