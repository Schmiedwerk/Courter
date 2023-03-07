using CourterClient.ApiClient;
using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Linq;
using System.Text;
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

        public SlotButtonData IsBookingPast(SlotButtonData button, ApiResponse<IEnumerable<TimeslotOut>> allTimeslots, DateTime timeNow)
        {
            if (allTimeslots.Result != null)
            {
                TimeslotOut time;
                foreach (var item in allTimeslots.Result.ToList())
                {
                    if (Today == DateOnly.FromDateTime(timeNow) && TimeOnly.FromDateTime(timeNow) > item.Start)
                    {
                        if (item.id == button.SlotId)
                        {
                            button.EnableButton = false;
                        }
                    }
                    else if (Today < DateOnly.FromDateTime(timeNow))
                    {
                        if (item.id == button.SlotId)
                        {
                            button.EnableButton = false;
                        }
                    }
                }
            }
            return button;
        }
    }
}
