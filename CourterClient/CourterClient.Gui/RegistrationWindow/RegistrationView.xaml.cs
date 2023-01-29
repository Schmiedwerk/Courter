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
    }
}
