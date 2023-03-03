using CourterClient.ApiClient;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Security.Cryptography.X509Certificates;
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
    public partial class CreateCourt : Window
    {
        public string? selectedSurface { get; set; }
        TransferCourtIn transfer;
        public CreateCourt(TransferCourtIn courtTransfer)
        {
            InitializeComponent();
            this.transfer = courtTransfer;
        }

        private void Button_Click(object sender, RoutedEventArgs e)
        {
            string name = NameInput.Text;
            string? surface = selectedSurface;
            if (name.Length != 0 && surface != null) 
            {
                CourtIn newCourt = new CourtIn(name, surface);
                transfer.Invoke(newCourt);
                this.Close();
            }
            else
            {
                MessageBox.Show("Erstellen fehlgeschlagen: \nGeben Sie einen Feldnamen ein und wählen Sie einen Untergrund.", "Erstellen fehlgeschlagen.");
            }
        }

        private void Selector_Checked(object sender, RoutedEventArgs e)
        {
            if(SandSelector.IsChecked == true)
            {
                selectedSurface = "Sand";
                GrassSelector.IsChecked = false;
                HardSelector.IsChecked = false;
                CarpetSelector.IsChecked = false;
                ArtificialSelector.IsChecked = false;
            }
            else if(GrassSelector.IsChecked == true)
            {
                selectedSurface = "Rasen";
                SandSelector.IsChecked = false;
                HardSelector.IsChecked = false;
                CarpetSelector.IsChecked = false;
                ArtificialSelector.IsChecked = false;
            }
            else if(HardSelector.IsChecked == true)
            {
                selectedSurface = "Hardbelag";
                GrassSelector.IsChecked = false;
                CarpetSelector.IsChecked = false;
                SandSelector.IsChecked = false;
                ArtificialSelector.IsChecked = false;
            }
            else if(CarpetSelector.IsChecked == true)
            {
                selectedSurface = "Teppich";
                SandSelector.IsChecked = false;
                HardSelector.IsChecked = false;
                GrassSelector.IsChecked = false;
                ArtificialSelector.IsChecked = false;
            }
            else if (ArtificialSelector.IsChecked == true)
            {
                selectedSurface = "Kunstbelag";
                SandSelector.IsChecked = false;
                HardSelector.IsChecked = false;
                GrassSelector.IsChecked = false;
                CarpetSelector.IsChecked = false;
            }
        }
    }
}
