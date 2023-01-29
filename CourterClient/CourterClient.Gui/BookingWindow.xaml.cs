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
using System.Windows.Navigation;
using System.Windows.Shapes;

namespace CourterClient.Gui
{
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class BookingWindow : Window
    {
        public BookingWindow()
        {
            InitializeComponent();
        }
        private void BookCourt(object sender, RoutedEventArgs e)
        {
            this.Close();
        }
        private void CancelBook(object sender, RoutedEventArgs e)
        {
            this.Close();
        }
        private void OnKeyDown(object sender, System.Windows.Input.KeyEventArgs e)
        {
            if (e.Key == Key.Enter)
            {                
                Console.WriteLine("you pressed enter to");
                BookCourt(this, new RoutedEventArgs());
            }
        }
    }
}
