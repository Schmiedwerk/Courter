using CourterClient.ApiClient;
using System;
using System.Collections.Generic;
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
        public bool IsClosing { get; set; }
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

        public void IsBookingPast(List<TimeslotOut> allTimeslots, DateTime timeNow)
        {
            TimeslotOut time;
            foreach (var item in allTimeslots)
            {
                if (Today == DateOnly.FromDateTime(timeNow) && TimeOnly.FromDateTime(timeNow) > item.Start)
                {
                    if (item.id == SlotId)
                    {
                        EnableButton = false;
                    }
                }
                else if (Today < DateOnly.FromDateTime(timeNow))
                {
                    if (item.id == SlotId)
                    {
                        EnableButton = false;
                    }
                }
            }
        }

        public void CheckBooking(List<BookingOut> todaysBookings, TimeSlot slot)
        {
            foreach (var item in todaysBookings)
            {
                if (item.TimeslotId == slot.Id)
                {
                    if (item.CustomerId != null)
                    {
                        IsBooked = true;
                        IsOwnBooking = true;
                    }
                    IsBooked = true;
                }
            }
        }

        public void CheckClosings(List<ClosingOut> todaysClosings, TimeSlot slot)
        {
            foreach (var item in todaysClosings)
            {
                if (item.StartTimeslotId <= slot.Id && item.EndTimeslotId >= slot.Id)
                {
                    IsClosing = true;
                }
            }
        }

        public List<BookingOut> GetTodaysBookingOuts(List<BookingOut> AllBookings)
        {
            List<BookingOut> todaysBookings = new List<BookingOut>();

            foreach (var item in AllBookings)
            {
                if (item.Date == Today && item.CourtId == CourtId)
                {
                    todaysBookings.Add(item);
                }
            }

            return todaysBookings;
        }
    }
}
