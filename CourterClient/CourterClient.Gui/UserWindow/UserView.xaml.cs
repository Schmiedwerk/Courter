using CourterClient.Gui.CalendarWindow;
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

namespace CourterClient.Gui.UserWindow
{
    public partial class UserView : Window
    {
        public List<string> courts = new List<string>();
        public List<string> slots = new List<string>();

        public UserView()
        {
            InitializeComponent();
            FillCourts();
            FillSlots();
        }

        public void FillCourts()
        {
            courts.Append("Wimbledon");
            courts.Append("New York");
            courts.Append("Melbourne");
            courts.Append("Paris");
        }

        public void FillSlots()
        {
            for(int i = 10; i <= 22; i++)
            {
                slots.Append($"{i}:00 - {i + 1}:00");
            }
        }

        private void Image_MouseUp(object sender, MouseButtonEventArgs e)
        {
            this.Close();
        }

        private void Image_MouseUp_1(object sender, MouseButtonEventArgs e)
        {
            var cal = new CalendarView();
            cal.ShowDialog();
        }
    }
}
