using CourterClient.ApiClient;
using CourterClient.Gui.Gui;
using CourterClient.Gui.Gui.AdminWindow;
using CourterClient.Gui.RegistrationWindow;
using CourterClient.Gui.UserWindow;
using Microsoft.Extensions.DependencyInjection;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Shapes;

namespace CourterClient.Gui.LoginWindow
{
    public partial class LoginView : Window
    {
        public LoginView()
        {
            InitializeComponent();
        }

        private void textUserName_MouseDown(object sender, MouseButtonEventArgs e)
        {
            textInputBox.Focus();
        }

        private void textInputBox_TextChanged(object sender, TextChangedEventArgs e)
        {
            if(!string.IsNullOrEmpty(textInputBox.Text) && textInputBox.Text.Length > 0) 
            {
                textUserName.Visibility = Visibility.Collapsed;
            }
            else
            {
                textUserName.Visibility = Visibility.Visible;
            }
        }

        private void textPw_MouseDown(object sender, MouseButtonEventArgs e)
        {
            pwInputBox.Focus();
        }

        private void pwInputBox_PasswordChanged(object sender, RoutedEventArgs e)
        {
            if (!string.IsNullOrEmpty(pwInputBox.Password) && pwInputBox.Password.Length > 0)
            {
                textPw.Visibility = Visibility.Collapsed;
            }
            else
            {
                textPw.Visibility = Visibility.Visible;
            }
        }

        private void Image_MouseUp(object sender, MouseButtonEventArgs e)
        {
            Application.Current.Shutdown();
        }

        private void Border_MouseDown(object sender, MouseButtonEventArgs e)
        {
            if (e.ChangedButton == MouseButton.Left)
                this.DragMove();
        }

        private void Button_Click(object sender, RoutedEventArgs e)
        {
            var registration = new RegistrationView();
            registration.ShowDialog();
        }

        private async void Button_Click_1(object sender, RoutedEventArgs e)
        {
            var rootClient = App.AppHost.Services.GetRequiredService<ClientManager>();

            string username = textInputBox.Text;
            string password = pwInputBox.Password;

            if(username.Length != 0 || password.Length != 0)
            {
                Credentials login = new Credentials(username, password);
                var response = await rootClient.clientManager.Login(login);

                if (response.Successful)
                {
                    if(response.Result == UserRole.Customer)
                    {
                        var UserWin = new UserView();
                        this.Close();
                        UserWin.ShowDialog();
                    }
                    else if(response.Result == UserRole.Employee)
                    {
                        var UserWin = new UserView();
                        this.Close();
                        UserWin.ShowDialog();
                    }
                    else if(response.Result == UserRole.Admin)
                    {
                        var vm = new AdminViewModel(rootClient);
                        var adminWin = new AdminView();
                        adminWin.DataContext= vm;
                        
                        await vm.FillTables();
                        
                        this.Close();
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
        }
    }
}
