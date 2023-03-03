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
    public partial class CreateTime : Window
    {
        TransferTimeslotIn timeTransfer;
        public CreateTime(TransferTimeslotIn timeTransfer)
        {
            InitializeComponent();
            this.timeTransfer = timeTransfer;
        }

        private void Button_Click(object sender, RoutedEventArgs e)
        {
            string start = this.StartInput.Text;
            string end = this.EndInput.Text;

            if(start.Length != 0 && end.Length != 0)
            {
                if(start.Length < 3 && end.Length < 3)
                {
                    start = $"{start}:00";
                    end = $"{end}:00";
                }
                TimeOnly dtStart = TimeOnly.Parse(start);
                TimeOnly dtEnd = TimeOnly.Parse(end);

                TimeslotIn newSlot = new TimeslotIn(dtStart, dtEnd);

                timeTransfer.Invoke(newSlot);

                this.Close();
            }

        }
    }
}
