using CourterClient.Gui.Gui;
using CourterClient.Gui.Gui.UserWindow;
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
    }
}
