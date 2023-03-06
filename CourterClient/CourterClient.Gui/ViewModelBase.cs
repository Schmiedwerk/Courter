using CourterClient.ApiClient;
using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Linq;
using System.Runtime.CompilerServices;
using System.Text;
using System.Threading.Tasks;

namespace CourterClient.Gui
{
    public delegate void TransferDate(DateOnly date);

    public delegate void TransferAdminCredentials(Credentials user);
    public delegate void TransferEmployeeCredentials(Credentials user);
    public delegate void TransferCourtIn(CourtIn court);
    public delegate void TransferTimeslotIn(TimeslotIn timeslot);

    public delegate void TransferGuestBooking(GuestBookingIn guestBooking);
    public delegate void TransferClosing(ClosingIn closing);

    public delegate Task TransferCourtDefinitionTrigger();

    public abstract class ViewModelBase : INotifyPropertyChanged
    {
        public event PropertyChangedEventHandler? PropertyChanged;

        protected virtual void RaisePropertyChanged([CallerMemberName] string propertyName = "")
        {
            if (!string.IsNullOrEmpty(propertyName))
                this.PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(propertyName));
        }
    }
}