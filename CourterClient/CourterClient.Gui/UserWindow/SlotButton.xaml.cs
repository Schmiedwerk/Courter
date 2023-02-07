using System.Windows;
using System.Windows.Controls;
using System.Windows.Input;
using System.Windows.Media;

namespace CourterClient.Gui.Gui.UserWindow
{
    public partial class SlotButton : UserControl
    {
        public bool IsBooked { get; set; }


        public SlotButton()
        {
            InitializeComponent();

            SetButtonState();
        }

        public void SetButtonState()
        {
            if (IsBooked == true)
            {
                this.StateButton.Background = Brushes.Firebrick;
            }
            else
            {
                this.StateButton.Background = Brushes.ForestGreen;
            }
        }

        public void SetBooked(bool isBooked)
        {
            this.IsBooked = isBooked;
            SetButtonState();
        }

        private void Button_Click(object sender, RoutedEventArgs e)
        {
            this.StateButton.Background = Brushes.Firebrick;
        }
    }
}
