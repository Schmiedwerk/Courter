using System;
using System.Windows;
using System.Windows.Controls.Primitives;
using System.Windows.Input;

namespace CourterClient.Gui.CalendarWindow
{
    public partial class CalendarView : Window
    {
        TransferDate transfer;

        public CalendarView(TransferDate del)
        {
            InitializeComponent();
            DataContext= this;
            transfer = del;
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

        private void Button_Click(object sender, RoutedEventArgs e)
        {
            var selected = CalendarWidget.SelectedDate ?? DateTime.Today;
            transfer.Invoke(DateOnly.FromDateTime(selected));
            
            this.Close();
        }

        private void CalendarWidget_GotMouseCapture(object sender, MouseEventArgs e)
        {
            UIElement? originalElement = e.OriginalSource as UIElement;
            if (originalElement is CalendarDayButton || originalElement is CalendarItem)
            {
                originalElement?.ReleaseMouseCapture();
            }
        }
    }
}
