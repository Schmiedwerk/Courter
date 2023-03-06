using System;
using System.Runtime.CompilerServices;
using System.Windows.Media;

namespace CourterClient.Gui.Gui.UserWindow
{
    public abstract class SlotButtonData : ViewModelBase
    {
        public string CourtName { get; set; }
        public int CourtId { get; set; }
        public int SlotId { get; set; }
        public bool IsBooked { get; set; }
        public bool IsOwnBooking { get; set; }
        public DateOnly Today { get; set; }

        private bool enableButton;
        public bool EnableButton
        {
            get => enableButton;
            set
            {
                if (enableButton != value)
                {
                    enableButton = value;
                    RaisePropertyChanged();
                }
            }
        }

        private SolidColorBrush backgroundColor;
        public SolidColorBrush BackgroundColor
        {
            get => backgroundColor;
            set
            {
                if (backgroundColor != value)
                {
                    backgroundColor = value;
                    RaisePropertyChanged();
                }
            }
        }

        public SlotButtonData(int id, bool isBooked, bool ownBooking, string courtname, int courtid, DateOnly current)
        {
            EnableButton = true;
            CourtName = courtname;
            CourtId = courtid;
            SlotId = id;
            IsBooked = isBooked;
            IsOwnBooking = ownBooking;
            
            Today = current;

            
        }

        public abstract void SetState();

        public void ChangeState(bool booking)
        {
            this.IsBooked = booking;

            SetState();
        }


        public DelegateCommand BookingButtonClicked { get; set; }

    }
}
