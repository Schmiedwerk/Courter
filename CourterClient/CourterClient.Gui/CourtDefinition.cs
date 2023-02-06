using CourterClient.Gui.Gui.UserWindow;
using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace CourterClient.Gui.Gui
{
    public class CourtDefinition : ViewModelBase
    {
        public string CourtName { get; set; }
        private int Slots = 0;

        private ObservableCollection<SlotButton> slotList = new ObservableCollection<SlotButton>();

        public ObservableCollection<SlotButton> SlotList
        {
            get => slotList;
            set
            {
                if(slotList!= value)
                {
                    slotList = value;
                    this.RaisePropertyChanged();
                }
            }
        }

        public CourtDefinition(string courtName, int slots)
        {
            CourtName = courtName;
            Slots = slots;
            FillCourtSlots();
        }

        public void FillCourtSlots()
        {
            this.SlotList = new ObservableCollection<SlotButton>();
            {
                for (int i = 0; i < Slots; i++)
                {
                    SlotButton slotButton = new SlotButton();
                    slotButton.SetBooked(true);
                    SlotList.Add(slotButton);
                }
            }
        }
    }
}
