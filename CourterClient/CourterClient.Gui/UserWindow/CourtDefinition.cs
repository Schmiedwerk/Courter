using CourterClient.ApiClient;
using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Linq;
using System.Threading.Tasks;

namespace CourterClient.Gui.Gui.UserWindow
{
    public abstract class CourtDefinition : ViewModelBase
    {
        public string CourtName { get; set; }
        public int CourtId { get; set; }
        public List<TimeSlot> Slots { get; set; }
        public DateOnly Today { get; set; }

        private ObservableCollection<SlotButtonData> slotList = new ObservableCollection<SlotButtonData>();

        public ObservableCollection<SlotButtonData> SlotList
        {
            get => slotList;
            set
            {
                if (slotList != value)
                {
                    slotList = value;
                    RaisePropertyChanged();
                }
            }
        }

        public CourtDefinition(string courtName, int id, List<TimeSlot> slots, DateOnly current)
        {
            CourtName = courtName;
            CourtId = id;
            Slots = slots;
            Today = current;
        }

        public abstract Task FillCourtSlots();

        public SlotButtonData CheckClosings(SlotButtonData button, List<ClosingOut> todaysClosings, TimeSlot slot)
        {
            foreach (var item in todaysClosings)
            {
                if (item.StartTimeslotId <= slot.Id && item.EndTimeslotId >= slot.Id)
                {
                    button.IsClosing = true;
                }
            }
            return button;
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

        public List<ClosingOut> GetTodaysClosingOuts(List<ClosingOut> AllClosingOuts)
        {
            List<ClosingOut> todaysClosings = new List<ClosingOut>();

            foreach (var close in AllClosingOuts)
            {
                if (close.Date == Today && close.CourtId == CourtId)
                {
                    todaysClosings.Add(close);
                }
            }

            return todaysClosings;
        }
    }
}
