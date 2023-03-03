using CourterClient.ApiClient;
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

namespace CourterClient.Gui.Gui.AdminWindow
{
    public partial class CreateUser : Window
    {
        TransferAdminCredentials? adminTransfer;
        TransferEmployeeCredentials? employeeTransfer;

        public CreateUser(TransferAdminCredentials admin)
        {
            InitializeComponent();
            this.adminTransfer = admin;
        }
        public CreateUser(TransferEmployeeCredentials employee)
        {
            InitializeComponent();
            this.employeeTransfer = employee;
        }

        private void Button_Click(object sender, RoutedEventArgs e)
        {
            string username = this.UsernameInput.Text;
            string password = this.PasswordInput.Password;

            if (username.Length != 0 && password.Length != 0)
            {
                Credentials newUser = new Credentials(username, password);
                if(adminTransfer != null)
                {
                    adminTransfer.Invoke(newUser);

                }
                else
                {
                    employeeTransfer.Invoke(newUser);
                }
                this.Close();
            }
            else
            {
                MessageBox.Show("Erstellen fehlgeschlagen: \nDie Felder dürfen nicht leer sein.", "Erstellen fehlgeschlagen.");
            }
        }
    }
}
