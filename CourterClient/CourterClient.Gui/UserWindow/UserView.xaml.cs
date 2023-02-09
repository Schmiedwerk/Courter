using CourterClient.Gui.Gui.UserWindow;
using System.Windows;
using System.Windows.Input;

namespace CourterClient.Gui.UserWindow
{
    public partial class UserView : Window
    {
        public UserView()
        {
            InitializeComponent();
            this.DataContext = new UserViewModel();
        }

        private void Image_MouseUp(object sender, MouseButtonEventArgs e)
        {
            this.Close();
        }

        private void Border_MouseDown(object sender, MouseButtonEventArgs e)
        {
            if (e.ChangedButton == MouseButton.Left)
                this.DragMove();
        }
    }
}
