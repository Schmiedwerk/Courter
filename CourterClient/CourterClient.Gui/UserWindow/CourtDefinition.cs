using CourterClient.ApiClient;
using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace CourterClient.Gui.Gui.UserWindow
{
    public class CourtDefinition : ViewModelBase
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

    }
}
