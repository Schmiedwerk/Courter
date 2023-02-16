using CourterClient.ApiClient;
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
            string _serverUrl = "http://localhost:8000";
            RootClient rootClient = new RootClient(_serverUrl);

            string username = textInputBox.Text;
            string password;

            if(pwInputBox.Password == pwInputBox2.Password && pwInputBox.Password.Length > 0)
            {
                password = pwInputBox.Password;
                Credentials newUser = new Credentials(username, password);
                var response = await rootClient.SignUp(newUser);

                if(response.Successful)
                {
                    var user = response.Result;
                    MessageBox.Show($"Benutzer: {user?.Username}\nid: {user?.Id} \nErfolgreich erstellt!", "Benutzer erstellt!");
                    this.Close();
                }
                else
                {
                    MessageBox.Show($"Anmeldung fehlgeschlagen: {response.Detail}", "Anmelden fehlgeschlagen.");
                }
            }
            else
            {
                MessageBox.Show("Ungültiges Passwort, erneut versuchen", "Anmelden fehlgeschlagen.");
            }
        }
    }
}
