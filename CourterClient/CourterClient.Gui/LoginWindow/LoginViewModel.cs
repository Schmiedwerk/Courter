using CourterClient.ApiClient;
using CourterClient.Gui.Gui.AdminWindow;
using CourterClient.Gui.Gui.UserWindow;
using CourterClient.Gui.Gui;
using CourterClient.Gui.UserWindow;
using Microsoft.Extensions.DependencyInjection;
using System.ComponentModel;
using System.Runtime.CompilerServices;
using System.Security;
using System.Windows;
using System.Windows.Input;
using System;
using CourterClient.Gui.RegistrationWindow;

namespace CourterClient.Gui.LoginWindow
{
    public class LoginViewModel : ViewModelBase
    {
        private string username;

        public string Username
        {
            get => username;
            set
            {
                if (username != value)
                {
                    username = value;
                    RaisePropertyChanged();
                }
            }
        }

        public LoginViewModel()
        {
            Register = new DelegateCommand((o) =>
            {
                var registration = new RegistrationView();
                registration.ShowDialog();
            });

            Login = new DelegateCommand(async (o) =>
            {
                var rootClient = App.AppHost.Services.GetRequiredService<ClientManager>();
                var loginView = App.AppHost.Services.GetRequiredService<LoginView>();

                string Password = loginView.pwInputBox.Password;

                if (Username.Length != 0 || Password.Length != 0)
                {
                    Credentials login = new Credentials(Username, Password);
                    var response = await rootClient.clientManager.Login(login);

                    if (response.Successful)
                    {
                        var publicClient = rootClient.clientManager.MakePublicClient();
                        if (response.Result == UserRole.Customer)
                        {
                            var customerClient = rootClient.clientManager.MakeCustomerClient();
                            var userVm = new UserViewModel(publicClient, customerClient);
                            var UserWin = new UserView();

                            await userVm.CreateTimeTable();
                            await userVm.CreateCourtTable();
                            UserWin.DataContext = userVm;

                            loginView.Close();
                            UserWin.ShowDialog();
                        }
                        else if (response.Result == UserRole.Employee)
                        {
                            var employeeClient = rootClient.clientManager.MakeEmployeeClient();
                            var userVm = new UserViewModel(publicClient, employeeClient);
                            var UserWin = new UserView();

                            await userVm.CreateTimeTable();

                            await userVm.CreateCourtTable();
                            UserWin.DataContext = userVm;

                            loginView.Close();
                            UserWin.ShowDialog();
                        }
                        else if (response.Result == UserRole.Admin)
                        {
                            var adminClient = rootClient.clientManager.MakeAdminClient();

                            var adminVm = new AdminViewModel(publicClient, adminClient);
                            var adminWin = new AdminView();
                            adminWin.DataContext = adminVm;

                            await adminVm.FillTables();

                            loginView.Close();
                            adminWin.ShowDialog();
                        }
                    }
                    else
                    {
                        MessageBox.Show($"Login fehlgeschlagen: \n{response.Detail}", "Login fehlgeschlagen");
                    }
                }
                else
                {
                    MessageBox.Show($"Login fehlgeschlagen: \nBenutzername oder Password ungültig", "Login fehlgeschlagen");
                }
            });
        }

        public DelegateCommand Login { get; set; }

        public DelegateCommand Register { get; set; }
    }
}