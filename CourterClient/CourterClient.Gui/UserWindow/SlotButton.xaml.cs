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
            var green = (SolidColorBrush)new BrushConverter().ConvertFromString("#6f916f");
            var red = (SolidColorBrush)new BrushConverter().ConvertFromString("#EE5C42");
            if (IsBooked == true)
            {
                this.StateButton.Background = red;
            }
            else
            {
                this.StateButton.Background = green;
            }
        }

        public void SetBooked(bool isBooked)
        {
            this.IsBooked = isBooked;
            SetButtonState();
        }

        private void Button_Click(object sender, RoutedEventArgs e)
        {
            SetBooked(true);
        }
    }
}
