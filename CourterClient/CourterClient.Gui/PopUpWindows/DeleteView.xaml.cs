using System.Collections.Generic;
using System.Windows;
using System.Windows.Input;

namespace CourterClient.Gui.Gui.PopUpWindows
{
    public partial class DeleteView : Window
    {
        TransferResponse transferResponse;
        public DeleteView(List<string> input, TransferResponse transfer)
        {
            InitializeComponent();
            SetInput(input);
            this.transferResponse = transfer;
        }

        public void SetInput(List<string> input)
        {
            this.Header.Text = input[0];
            this.Date.Text = input[1];
            this.Field.Text = input[2];
            this.Start.Text = input[3];
            this.End.Text = input[4];
        }

        private void Close_Click(object sender, RoutedEventArgs e)
        {
            transferResponse.Invoke(false);
            this.Close();
        }

        private void Image_MouseUp(object sender, MouseButtonEventArgs e)
        {
            transferResponse.Invoke(false);
            this.Close();
        }

        private void Border_MouseDown(object sender, MouseButtonEventArgs e)
        {
            if (e.ChangedButton == MouseButton.Left)
                this.DragMove();
        }

        private void Button_Click(object sender, RoutedEventArgs e)
        {
            transferResponse.Invoke(true);
            this.Close();
        }
    }
}
