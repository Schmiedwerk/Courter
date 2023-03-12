using CourterClient.ApiClient;
using CourterClient.Gui.Gui;
using CourterClient.Gui.Gui.PopUpWindows;
using Microsoft.Extensions.DependencyInjection;
using System.Collections.Generic;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Input;

namespace CourterClient.Gui.RegistrationWindow
{
    public partial class RegistrationView : Window
    {
        public RegistrationView()
        {
            InitializeComponent();
        }

        private void textUserName_MouseDown(object sender, MouseButtonEventArgs e)
        {
            textInputBox.Focus();
        }

        private void textInputBox_TextChanged(object sender, TextChangedEventArgs e)
        {
            if (!string.IsNullOrEmpty(textInputBox.Text) && textInputBox.Text.Length > 0)
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

        private void textPw2_MouseDown(object sender, MouseButtonEventArgs e)
        {
            pwInputBox2.Focus();
        }

        private void pwInputBox2_PasswordChanged(object sender, RoutedEventArgs e)
        {
            if (!string.IsNullOrEmpty(pwInputBox2.Password) && pwInputBox2.Password.Length > 0)
            {
                textPw2.Visibility = Visibility.Collapsed;
            }
            else
            {
                textPw2.Visibility = Visibility.Visible;
            }
        }

        private void Border_MouseDown(object sender, MouseButtonEventArgs e)
        {
            if (e.ChangedButton == MouseButton.Left)
                this.DragMove();
        }

        private void Image_MouseUp(object sender, MouseButtonEventArgs e)
        {
            this.Close();
        }

        private async void CreateButton(object sender, RoutedEventArgs e)
        {
            
            var rootClient = App.AppHost.Services.GetRequiredService<ClientManager>();

            string username = textInputBox.Text;
            string password;


            if(pwInputBox.Password.Length < 5)
            {
                MessageBox.Show("Anmeldung fehlgeschlagen: \nDas Passwort muss mindestens 5 Zeichen lang sein.", "Anmelden fehlgeschlagen.");
            }
            else
            {
                if (pwInputBox.Password == pwInputBox2.Password && pwInputBox.Password.Length > 0)
                {

                    password = pwInputBox.Password;
                    Credentials newUser = new Credentials(username, password);
                    var response = await rootClient.clientManager.SignUp(newUser);

                    if (response.Successful)
                    {
                        var user = response.Result;
                        List<string> infoList = new List<string>();
                        infoList.Add("Benutzer erstellt:");
                        infoList.Add(user.Username);
                        infoList.Add("Benutzer erfolgreich erstellt!");
                        var info = new CreateInfoView(infoList);
                        info.ShowDialog();
                        this.Close();
                    }
                    else
                    {
                        List<string> infoList = new List<string>();
                        infoList.Add("Anmeldung fehlgeschlagen: ");
                        infoList.Add($"Fehler {response.Detail}");

                        var view = new LoginErrorView(infoList);
                        view.ShowDialog();
                    }
                }
                else
                {
                    List<string> infoList = new List<string>();
                    infoList.Add("Anmeldung fehlgeschlagen: ");
                    infoList.Add("Die Passwörter stimmen nicht überein.");

                    var view = new LoginErrorView(infoList);
                    view.ShowDialog();
                }
            }

        }
    }
}
